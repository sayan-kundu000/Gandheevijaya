from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.api.deps import verify_owner_or_admin
from backend.app.core.exceptions import ConflictException, NotFoundException, ValidationException
from backend.app.models.attempt import Attempt, AttemptAnswer
from backend.app.models.performance import StudentSubjectPerformance, StudentTopicPerformance
from backend.app.models.quiz import Quiz
from backend.app.models.user import User
from backend.app.repositories.quiz_repository import AttemptRepository, QuizRepository
from backend.app.schemas.quiz import (
    AttemptAnswerItem,
    QuestionReviewItem,
    QuizSubmitRequest,
    ResultResponse,
)
from backend.app.services.base import BaseService


class AttemptService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db)
        self.attempt_repo = AttemptRepository()
        self.quiz_repo = QuizRepository()

    def get_attempts(
        self,
        current_user: User,
        user_id: Optional[str] = None,
        quiz_id: Optional[int] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[Attempt], int]:
        # Non-admins can only see their own attempts
        if current_user.role != "ADMIN":
            target_user_id = current_user.id
        else:
            target_user_id = user_id

        return self.attempt_repo.get_multi_filtered(
            self.db, user_id=target_user_id, quiz_id=quiz_id, status=status, skip=skip, limit=limit
        )

    def get_attempt(self, attempt_id: str, current_user: User) -> Attempt:
        attempt = self.attempt_repo.get_with_details(self.db, attempt_id=attempt_id)
        if not attempt:
            raise NotFoundException(message=f"Attempt with ID {attempt_id} not found.")

        # Server-side IDOR check
        verify_owner_or_admin(resource_user_id=attempt.user_id, current_user=current_user)
        return attempt

    def submit_quiz_attempt(
        self, attempt_id: str, payload: QuizSubmitRequest, current_user: User
    ) -> ResultResponse:
        """
        Transactional server-side quiz submission evaluation.
        Evaluates answers against Question.correct_answer, calculates total score,
        marks attempt as SUBMITTED, and updates performance analytics.
        """
        def _action():
            attempt = self.attempt_repo.get_with_details(self.db, attempt_id=attempt_id)
            if not attempt:
                raise NotFoundException(message=f"Attempt with ID {attempt_id} not found.")

            verify_owner_or_admin(resource_user_id=attempt.user_id, current_user=current_user)

            if attempt.status == "SUBMITTED":
                raise ConflictException(message="This quiz attempt has already been finalized and submitted.")

            quiz = attempt.quiz
            if not quiz:
                quiz = self.quiz_repo.get_with_questions(self.db, quiz_id=attempt.quiz_id)

            # Map submitted answers by question_id
            submitted_map: Dict[str, Optional[str]] = {
                ans.question_id: ans.selected_answer for ans in payload.answers
            }

            total_score = 0.0
            total_marks = quiz.total_marks or 0.0
            correct_count = 0
            incorrect_count = 0
            unanswered_count = 0
            review_items: List[QuestionReviewItem] = []

            # Map question associations
            assoc_map = {assoc.question_id: assoc for assoc in quiz.question_associations}

            for assoc in quiz.question_associations:
                q = assoc.question
                if not q:
                    continue

                selected_ans = submitted_map.get(q.id)
                is_correct = False
                marks_awarded = 0.0

                if not selected_ans or not selected_ans.strip():
                    unanswered_count += 1
                else:
                    # Evaluate correctness (case-insensitive string comparison or exact key)
                    correct_target = str(q.correct_answer).strip()
                    submitted_target = str(selected_ans).strip()

                    if correct_target.lower() == submitted_target.lower():
                        is_correct = True
                        marks_awarded = assoc.marks
                        correct_count += 1
                    else:
                        is_correct = False
                        marks_awarded = -abs(assoc.negative_marks)
                        incorrect_count += 1

                total_score += marks_awarded

                # Create AttemptAnswer record
                ans_record = AttemptAnswer(
                    attempt_id=attempt.id,
                    question_id=q.id,
                    selected_answer=selected_ans,
                    is_correct=is_correct,
                    marks_awarded=marks_awarded,
                )
                self.db.add(ans_record)

                # Prepare review item for result
                review_items.append(
                    QuestionReviewItem(
                        question_id=q.id,
                        question_text=q.question_text,
                        options=q.options,
                        selected_answer=selected_ans,
                        correct_answer=q.correct_answer,
                        is_correct=is_correct,
                        marks_awarded=marks_awarded,
                        marks_possible=assoc.marks,
                        explanation=q.explanation,
                    )
                )

            # Update Attempt model
            now = datetime.now(timezone.utc)
            attempt.completed_at = now
            attempt.score = round(total_score, 2)
            attempt.passed = total_score >= quiz.passing_score
            attempt.status = "SUBMITTED"

            # Update StudentSubjectPerformance
            self._update_subject_performance(user_id=attempt.user_id, subject_id=quiz.subject_id, score=attempt.score)

            self.db.flush()

            percentage = round((total_score / total_marks * 100.0), 2) if total_marks > 0 else 0.0

            return ResultResponse(
                attempt_id=attempt.id,
                quiz_id=quiz.id,
                quiz_title=quiz.title,
                user_id=attempt.user_id,
                user_name=current_user.full_name,
                started_at=attempt.started_at,
                completed_at=attempt.completed_at,
                score=attempt.score,
                total_marks=total_marks,
                percentage=percentage,
                passed=attempt.passed,
                total_questions=len(quiz.question_associations),
                correct_count=correct_count,
                incorrect_count=incorrect_count,
                unanswered_count=unanswered_count,
                detailed_questions=review_items,
            )

        return self.execute_in_transaction(_action)

    def get_result(self, attempt_id: str, current_user: User) -> ResultResponse:
        """Retrieves detailed result breakdown for a finalized attempt with server-side IDOR check."""
        attempt = self.attempt_repo.get_with_details(self.db, attempt_id=attempt_id)
        if not attempt:
            raise NotFoundException(message=f"Attempt with ID {attempt_id} not found.")

        verify_owner_or_admin(resource_user_id=attempt.user_id, current_user=current_user)

        if attempt.status != "SUBMITTED":
            raise ValidationException(message="Result is not available until the attempt has been submitted.")

        quiz = attempt.quiz
        assoc_map = {assoc.question_id: assoc for assoc in quiz.question_associations}

        correct_count = 0
        incorrect_count = 0
        unanswered_count = 0
        review_items: List[QuestionReviewItem] = []

        for ans in attempt.answers:
            q = ans.question
            assoc = assoc_map.get(ans.question_id)
            marks_possible = assoc.marks if assoc else 1.0

            if not ans.selected_answer:
                unanswered_count += 1
            elif ans.is_correct:
                correct_count += 1
            else:
                incorrect_count += 1

            review_items.append(
                QuestionReviewItem(
                    question_id=ans.question_id,
                    question_text=q.question_text if q else "",
                    options=q.options if q else None,
                    selected_answer=ans.selected_answer,
                    correct_answer=q.correct_answer if q else "",
                    is_correct=ans.is_correct,
                    marks_awarded=ans.marks_awarded,
                    marks_possible=marks_possible,
                    explanation=q.explanation if q else "",
                )
            )

        total_marks = quiz.total_marks or 0.0
        percentage = round((attempt.score / total_marks * 100.0), 2) if total_marks > 0 else 0.0

        return ResultResponse(
            attempt_id=attempt.id,
            quiz_id=quiz.id,
            quiz_title=quiz.title,
            user_id=attempt.user_id,
            user_name=attempt.quiz.subject.name if attempt.quiz and attempt.quiz.subject else None,
            started_at=attempt.started_at,
            completed_at=attempt.completed_at,
            score=attempt.score,
            total_marks=total_marks,
            percentage=percentage,
            passed=attempt.passed,
            total_questions=len(quiz.question_associations),
            correct_count=correct_count,
            incorrect_count=incorrect_count,
            unanswered_count=unanswered_count,
            detailed_questions=review_items,
        )

    def _update_subject_performance(self, user_id: str, subject_id: int, score: float) -> None:
        """Internal helper updating StudentSubjectPerformance metrics."""
        perf = self.db.scalar(
            select(StudentSubjectPerformance).where(
                StudentSubjectPerformance.user_id == user_id,
                StudentSubjectPerformance.subject_id == subject_id,
            )
        )
        if not perf:
            perf = StudentSubjectPerformance(
                user_id=user_id,
                subject_id=subject_id,
                total_quizzes_taken=1,
                average_score=score,
                completion_rate=100.0,
            )
            self.db.add(perf)
        else:
            prev_total = perf.total_quizzes_taken
            perf.total_quizzes_taken += 1
            perf.average_score = round(((perf.average_score * prev_total) + score) / perf.total_quizzes_taken, 2)
            perf.last_updated = datetime.now(timezone.utc)
