import random
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Tuple

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from backend.app.api.deps import verify_owner_or_admin
from backend.app.core.exceptions import ConflictException, ForbiddenException, NotFoundException, ValidationException
from backend.app.models.attempt import Attempt, AttemptAnswer
from backend.app.models.content import Question
from backend.app.models.performance import StudentSubjectPerformance, StudentTopicPerformance
from backend.app.models.quiz import Quiz, QuizQuestion
from backend.app.models.user import User
from backend.app.repositories.content_repository import QuestionRepository
from backend.app.repositories.quiz_repository import AttemptRepository, QuizRepository
from backend.app.schemas.common import MessageResponse
from backend.app.schemas.content import QuestionStudentResponse
from backend.app.schemas.quiz import (
    AttemptAnswerItem,
    AttemptAnswerResponse,
    AttemptResponse,
    AttemptResumeResponse,
    AttemptStartResponse,
    QuestionReviewItem,
    QuizSubmitRequest,
    ResultResponse,
    SingleResponseSubmitRequest,
    ToggleReviewRequest,
)
from backend.app.services.base import BaseService
from backend.app.services.question_selection_service import QuestionSelectionService
from backend.app.services.scoring_service import ScoringService


class AttemptManagementService(BaseService):
    """
    Comprehensive Quiz Attempt Lifecycle & Scoring Engine.
    Handles attempt creation, option randomization stabilization, response upsert,
    server-side timer/expiry, anti-tampering answer validation, final scoring with row locking,
    result generation, and analytics performance metrics updates.
    """

    def __init__(self, db: Session):
        super().__init__(db)
        self.quiz_repo = QuizRepository()
        self.attempt_repo = AttemptRepository()
        self.question_repo = QuestionRepository()
        self.selection_service = QuestionSelectionService(db)
        self.scoring_service = ScoringService()

    def start_quiz_attempt(
        self, quiz_id: int, user: User
    ) -> Tuple[Attempt, List[QuestionStudentResponse]]:
        """
        Starts a new attempt for a quiz.
        - Enforces publication status.
        - Enforces max attempts limit and single active attempt limit per user per quiz.
        - Snapshots assigned question order.
        - Stabilizes option order when randomize_options is enabled.
        - Calculates server-authoritative expiration timestamp.
        - Returns sanitized student question payload.
        """
        def _action():
            quiz = self.quiz_repo.get_with_questions(self.db, quiz_id=quiz_id)
            if not quiz:
                raise NotFoundException(message=f"Quiz with ID {quiz_id} not found.")

            if quiz.status != "PUBLISHED" and not quiz.is_published and user.role != "ADMIN":
                raise ForbiddenException(message="This quiz is not currently published.")

            # Check single active attempt constraint
            active_stmt = select(Attempt).where(
                Attempt.quiz_id == quiz.id,
                Attempt.user_id == user.id,
                Attempt.status == "IN_PROGRESS",
            )
            existing_active = self.db.scalar(active_stmt)
            if existing_active:
                # Check if it has expired
                now = datetime.now(timezone.utc)
                exp_dt = existing_active.expires_at.replace(tzinfo=timezone.utc) if existing_active.expires_at.tzinfo is None else existing_active.expires_at
                if now > exp_dt:
                    self._finalize_and_score_attempt(existing_active, status="EXPIRED")
                    self.db.commit()
                else:
                    # Seamlessly return existing active attempt and its assigned questions
                    resume_data = self.resume_quiz_attempt(attempt_id=existing_active.id, current_user=user)
                    return existing_active, resume_data.questions

            # Check max attempts limit if configured
            if quiz.max_attempts is not None and user.role != "ADMIN":
                completed_count_stmt = select(Attempt).where(
                    Attempt.quiz_id == quiz.id,
                    Attempt.user_id == user.id,
                    Attempt.status.in_(["SUBMITTED", "EXPIRED"]),
                )
                completed_attempts = len(list(self.db.scalars(completed_count_stmt).all()))
                if completed_attempts >= quiz.max_attempts:
                    raise ForbiddenException(
                        message=f"You have reached the maximum allowed attempts ({quiz.max_attempts}) for this quiz."
                    )

            # Determine questions to assign with deduplication
            assoc_list = sorted(quiz.question_associations, key=lambda a: a.sort_order)
            if assoc_list:
                seen_q_ids = set()
                selected_questions = []
                for a in assoc_list:
                    if a.question and a.question.id not in seen_q_ids:
                        seen_q_ids.add(a.question.id)
                        selected_questions.append(a.question)
            else:
                # Dynamically select questions if none associated statically
                count_to_select = quiz.question_count if quiz.question_count > 0 else 10
                selected_questions = self.selection_service.validate_and_select_questions(
                    requested_count=count_to_select,
                    exam_id=quiz.exam_id,
                    subject_id=quiz.subject_id,
                    topic_id=quiz.topic_id,
                    randomize=quiz.randomize_questions,
                )

            question_ids = [q.id for q in selected_questions]

            # Stabilize option ordering ONCE if option randomization enabled
            option_mappings = {}
            if quiz.randomize_options:
                for q in selected_questions:
                    if q.options and isinstance(q.options, list):
                        shuffled_opts = list(q.options)
                        random.shuffle(shuffled_opts)
                        option_mappings[q.id] = shuffled_opts

            now = datetime.now(timezone.utc)
            expires_at = now + timedelta(minutes=quiz.duration_minutes)

            total_possible_marks = quiz.total_marks or sum(
                next((a.marks for a in quiz.question_associations if a.question_id == q.id), 1.0)
                for q in selected_questions
            )

            attempt = Attempt(
                user_id=user.id,
                quiz_id=quiz.id,
                status="IN_PROGRESS",
                started_at=now,
                expires_at=expires_at,
                total_questions=len(question_ids),
                total_marks=total_possible_marks,
                question_order=question_ids,
                option_mappings=option_mappings if option_mappings else None,
            )
            self.db.add(attempt)
            self.db.flush()
            self.db.refresh(attempt)

            # Format student response payload applying stable option order
            student_questions = []
            for q in selected_questions:
                sq = QuestionStudentResponse.model_validate(q)
                if option_mappings and q.id in option_mappings:
                    sq.options = option_mappings[q.id]
                student_questions.append(sq)

            return attempt, student_questions

        return self.execute_in_transaction(_action)

    def submit_single_response(
        self, attempt_id: str, payload: SingleResponseSubmitRequest, current_user: User
    ) -> AttemptAnswerResponse:
        """
        Submits or updates a response to a single question during an active attempt.
        Validates attempt ownership, status, timer non-expiry, and question membership.
        """
        def _action():
            attempt = self.attempt_repo.get(self.db, id=attempt_id)
            if not attempt:
                raise NotFoundException(message=f"Attempt with ID {attempt_id} not found.")

            verify_owner_or_admin(resource_user_id=attempt.user_id, current_user=current_user)

            if attempt.status != "IN_PROGRESS":
                raise ConflictException(message=f"Cannot submit answers for an attempt with status '{attempt.status}'.")

            # Check server clock expiry
            now = datetime.now(timezone.utc)
            expires = attempt.expires_at.replace(tzinfo=timezone.utc) if attempt.expires_at.tzinfo is None else attempt.expires_at
            if now > expires:
                self._finalize_and_score_attempt(attempt, status="EXPIRED")
                self.db.commit()
                raise ForbiddenException(message="Quiz time has expired. Your attempt has been automatically finalized.")

            # Validate question belongs to attempt
            if attempt.question_order and payload.question_id not in attempt.question_order:
                raise ValidationException(
                    message=f"Question ID '{payload.question_id}' does not belong to this quiz attempt."
                )

            # Upsert AttemptAnswer
            ans_stmt = select(AttemptAnswer).where(
                AttemptAnswer.attempt_id == attempt.id,
                AttemptAnswer.question_id == payload.question_id,
            )
            ans_record = self.db.scalar(ans_stmt)

            if ans_record:
                ans_record.selected_answer = payload.selected_answer
                ans_record.answered_at = now
            else:
                ans_record = AttemptAnswer(
                    attempt_id=attempt.id,
                    question_id=payload.question_id,
                    selected_answer=payload.selected_answer,
                    answered_at=now,
                )
                self.db.add(ans_record)

            self.db.flush()
            self.db.refresh(ans_record)
            return ans_record

        return self.execute_in_transaction(_action)

    def toggle_review_status(
        self, attempt_id: str, payload: ToggleReviewRequest, current_user: User
    ) -> MessageResponse:
        """Toggles the marked_for_review status on a question response."""
        def _action():
            attempt = self.attempt_repo.get(self.db, id=attempt_id)
            if not attempt:
                raise NotFoundException(message=f"Attempt with ID {attempt_id} not found.")

            verify_owner_or_admin(resource_user_id=attempt.user_id, current_user=current_user)

            ans_stmt = select(AttemptAnswer).where(
                AttemptAnswer.attempt_id == attempt.id,
                AttemptAnswer.question_id == payload.question_id,
            )
            ans_record = self.db.scalar(ans_stmt)

            if ans_record:
                ans_record.marked_for_review = payload.marked_for_review
            else:
                ans_record = AttemptAnswer(
                    attempt_id=attempt.id,
                    question_id=payload.question_id,
                    marked_for_review=payload.marked_for_review,
                )
                self.db.add(ans_record)

            self.db.flush()
            return MessageResponse(message=f"Question '{payload.question_id}' review status updated to {payload.marked_for_review}.")

        return self.execute_in_transaction(_action)

    def resume_quiz_attempt(
        self, attempt_id: str, current_user: User
    ) -> AttemptResumeResponse:
        """
        Resumes an active attempt, returning stored question order, option mappings,
        answered status map, remaining time seconds, and sanitized question list.
        """
        attempt = self.attempt_repo.get_with_details(self.db, attempt_id=attempt_id)
        if not attempt:
            raise NotFoundException(message=f"Attempt with ID {attempt_id} not found.")

        verify_owner_or_admin(resource_user_id=attempt.user_id, current_user=current_user)

        now = datetime.now(timezone.utc)
        expires = attempt.expires_at.replace(tzinfo=timezone.utc) if attempt.expires_at.tzinfo is None else attempt.expires_at

        # Check server clock expiry
        if attempt.status == "IN_PROGRESS" and now > expires:
            self._finalize_and_score_attempt(attempt, status="EXPIRED")
            self.db.commit()

        # Retrieve questions in snapshot order applying stable option mappings with deduplication
        q_order = attempt.question_order or []
        option_map = attempt.option_mappings or {}
        questions = []
        seen_resumed_ids = set()
        if q_order:
            for q_id in q_order:
                if q_id not in seen_resumed_ids:
                    seen_resumed_ids.add(q_id)
                    q = self.question_repo.get(self.db, id=q_id)
                    if q:
                        sq = QuestionStudentResponse.model_validate(q)
                        if option_map and q.id in option_map:
                            sq.options = option_map[q.id]
                        questions.append(sq)
        elif attempt.quiz:
            for assoc in sorted(attempt.quiz.question_associations, key=lambda a: a.sort_order):
                if assoc.question and assoc.question.id not in seen_resumed_ids:
                    seen_resumed_ids.add(assoc.question.id)
                    q = assoc.question
                    sq = QuestionStudentResponse.model_validate(q)
                    if option_map and q.id in option_map:
                        sq.options = option_map[q.id]
                    questions.append(sq)

        answers_map = {ans.question_id: ans.selected_answer for ans in attempt.answers}
        review_map = {ans.question_id: ans.marked_for_review for ans in attempt.answers}

        remaining_sec = max(0, int((expires - now).total_seconds())) if attempt.status == "IN_PROGRESS" else 0

        attempt_resp = AttemptResponse.model_validate(attempt)
        attempt_resp.remaining_seconds = remaining_sec

        return AttemptResumeResponse(
            attempt=attempt_resp,
            questions=questions,
            answers_map=answers_map,
            review_map=review_map,
        )

    def submit_quiz_attempt(
        self, attempt_id: str, payload: Optional[QuizSubmitRequest], current_user: User
    ) -> ResultResponse:
        """
        Finalizes and scores a quiz attempt server-side with database row-level locking.
        Idempotent: If attempt is already SUBMITTED, returns existing result.
        """
        def _action():
            # Use row lock to prevent race conditions from concurrent submission requests
            attempt_stmt = (
                select(Attempt)
                .where(Attempt.id == attempt_id)
                .options(joinedload(Attempt.quiz), joinedload(Attempt.answers))
                .with_for_update()
            )
            attempt = self.db.scalar(attempt_stmt)
            if not attempt:
                raise NotFoundException(message=f"Attempt with ID {attempt_id} not found.")

            verify_owner_or_admin(resource_user_id=attempt.user_id, current_user=current_user)

            if attempt.status == "SUBMITTED":
                return self._build_result_response(attempt)

            # If client passed answers in bulk submit payload, update them first
            if payload and payload.answers:
                now = datetime.now(timezone.utc)
                for ans_item in payload.answers:
                    ans_stmt = select(AttemptAnswer).where(
                        AttemptAnswer.attempt_id == attempt.id,
                        AttemptAnswer.question_id == ans_item.question_id,
                    )
                    record = self.db.scalar(ans_stmt)
                    if record:
                        record.selected_answer = ans_item.selected_answer
                        record.answered_at = now
                    else:
                        record = AttemptAnswer(
                            attempt_id=attempt.id,
                            question_id=ans_item.question_id,
                            selected_answer=ans_item.selected_answer,
                            answered_at=now,
                        )
                        self.db.add(record)
                self.db.flush()

            # Execute final scoring evaluation
            return self._finalize_and_score_attempt(attempt, status="SUBMITTED")

        return self.execute_in_transaction(_action)

    def _finalize_and_score_attempt(self, attempt: Attempt, status: str) -> ResultResponse:
        """
        Core evaluation engine calculating score, penalty, percentage, accuracy,
        updating Attempt record, and refreshing student performance metrics.
        """
        quiz = attempt.quiz or self.quiz_repo.get_with_questions(self.db, quiz_id=attempt.quiz_id)
        if not quiz:
            raise NotFoundException(message=f"Quiz with ID {attempt.quiz_id} not found.")

        # Map question associations for custom marks / negative marking
        assoc_map = {assoc.question_id: assoc for assoc in quiz.question_associations}

        # Retrieve questions assigned to attempt
        q_ids = attempt.question_order or [assoc.question_id for assoc in quiz.question_associations]
        db_answers = list(self.db.scalars(select(AttemptAnswer).where(AttemptAnswer.attempt_id == attempt.id)).all())
        answers_by_q = {ans.question_id: ans for ans in db_answers}

        total_score = 0.0
        total_possible_marks = attempt.total_marks if attempt.total_marks > 0 else (quiz.total_marks or 0.0)
        correct_count = 0
        incorrect_count = 0
        unanswered_count = 0
        review_items: List[QuestionReviewItem] = []
        topic_stats: Dict[int, Dict[str, int]] = {}

        for q_id in q_ids:
            q = self.question_repo.get(self.db, id=q_id)
            if not q:
                continue

            assoc = assoc_map.get(q_id)
            marks_possible = assoc.marks if assoc else 1.0
            negative_marks = assoc.negative_marks if assoc else quiz.negative_marking

            ans_record = answers_by_q.get(q_id)
            selected_ans = ans_record.selected_answer if ans_record else None

            if not selected_ans or not str(selected_ans).strip():
                unanswered_count += 1
                is_correct = False
                marks_awarded = 0.0
                penalty = 0.0
            else:
                eval_res = self.scoring_service.evaluate_question_response(
                    question=q,
                    selected_answer=selected_ans,
                    marks_possible=marks_possible,
                    negative_marks=negative_marks,
                )
                is_correct = eval_res.is_correct
                marks_awarded = eval_res.marks_awarded
                penalty = eval_res.penalty_deducted
                if is_correct:
                    correct_count += 1
                else:
                    incorrect_count += 1

                # Track topic stats for analytics
                if q.topic_id:
                    if q.topic_id not in topic_stats:
                        topic_stats[q.topic_id] = {"attempted": 0, "correct": 0}
                    topic_stats[q.topic_id]["attempted"] += 1
                    if is_correct:
                        topic_stats[q.topic_id]["correct"] += 1

            total_score += marks_awarded

            # Save / update AttemptAnswer evaluation fields
            if not ans_record:
                ans_record = AttemptAnswer(
                    attempt_id=attempt.id,
                    question_id=q_id,
                    selected_answer=selected_ans,
                )
                self.db.add(ans_record)

            ans_record.is_correct = is_correct
            ans_record.marks_awarded = marks_awarded
            ans_record.penalty_deducted = penalty

            review_items.append(
                QuestionReviewItem(
                    question_id=q.id,
                    question_text=q.question_text,
                    options=attempt.option_mappings.get(q.id, q.options) if attempt.option_mappings else q.options,
                    selected_answer=selected_ans,
                    correct_answer=q.correct_answer,
                    is_correct=is_correct,
                    marks_awarded=marks_awarded,
                    penalty_deducted=penalty,
                    marks_possible=marks_possible,
                    explanation=q.explanation,
                )
            )

        now = datetime.now(timezone.utc)
        started_dt = attempt.started_at.replace(tzinfo=timezone.utc) if attempt.started_at.tzinfo is None else attempt.started_at
        time_taken = max(0, int((now - started_dt).total_seconds()))

        stats = ScoringService.calculate_summary_stats(
            total_questions=len(q_ids),
            correct_count=correct_count,
            incorrect_count=incorrect_count,
            unanswered_count=unanswered_count,
            total_score=total_score,
            total_possible_marks=total_possible_marks,
        )

        attempt.completed_at = now
        attempt.status = status
        attempt.score = round(total_score, 2)
        attempt.attempted_count = stats["attempted_count"]
        attempt.correct_count = correct_count
        attempt.incorrect_count = incorrect_count
        attempt.unanswered_count = unanswered_count
        attempt.percentage = stats["percentage"]
        attempt.accuracy = stats["accuracy"]
        attempt.time_taken_seconds = time_taken
        attempt.passed = total_score >= quiz.passing_score

        # Update performance analytics (Subject & Topics)
        if quiz.subject_id:
            self._update_subject_performance(user_id=attempt.user_id, subject_id=quiz.subject_id, score=attempt.score)

        for topic_id, t_data in topic_stats.items():
            self._update_topic_performance(
                user_id=attempt.user_id,
                topic_id=topic_id,
                attempted_delta=t_data["attempted"],
                correct_delta=t_data["correct"],
            )

        self.db.flush()

        return ResultResponse(
            attempt_id=attempt.id,
            quiz_id=quiz.id,
            quiz_title=quiz.title,
            user_id=attempt.user_id,
            started_at=attempt.started_at,
            completed_at=attempt.completed_at,
            status=attempt.status,
            total_questions=len(q_ids),
            attempted_count=attempt.attempted_count,
            correct_count=attempt.correct_count,
            incorrect_count=attempt.incorrect_count,
            unanswered_count=attempt.unanswered_count,
            total_marks=total_possible_marks,
            score=attempt.score,
            percentage=attempt.percentage,
            accuracy=attempt.accuracy,
            time_taken_seconds=time_taken,
            passed=attempt.passed,
            detailed_questions=review_items,
        )

    def _build_result_response(self, attempt: Attempt) -> ResultResponse:
        """Helper to construct ResultResponse for an already finalized attempt."""
        quiz = attempt.quiz or self.quiz_repo.get_with_questions(self.db, quiz_id=attempt.quiz_id)
        assoc_map = {assoc.question_id: assoc for assoc in (quiz.question_associations if quiz else [])}

        review_items: List[QuestionReviewItem] = []
        for ans in attempt.answers:
            q = ans.question or self.question_repo.get(self.db, id=ans.question_id)
            assoc = assoc_map.get(ans.question_id)
            marks_possible = assoc.marks if assoc else 1.0

            review_items.append(
                QuestionReviewItem(
                    question_id=ans.question_id,
                    question_text=q.question_text if q else "",
                    options=attempt.option_mappings.get(ans.question_id, q.options) if (attempt.option_mappings and q) else (q.options if q else None),
                    selected_answer=ans.selected_answer,
                    correct_answer=q.correct_answer if q else "",
                    is_correct=ans.is_correct,
                    marks_awarded=ans.marks_awarded,
                    penalty_deducted=ans.penalty_deducted,
                    marks_possible=marks_possible,
                    explanation=q.explanation if q else "",
                )
            )

        total_possible = attempt.total_marks if attempt.total_marks > 0 else (quiz.total_marks if quiz else 0.0)

        return ResultResponse(
            attempt_id=attempt.id,
            quiz_id=attempt.quiz_id,
            quiz_title=quiz.title if quiz else "Quiz Attempt",
            user_id=attempt.user_id,
            started_at=attempt.started_at,
            completed_at=attempt.completed_at,
            status=attempt.status,
            total_questions=attempt.total_questions,
            attempted_count=attempt.attempted_count,
            correct_count=attempt.correct_count,
            incorrect_count=attempt.incorrect_count,
            unanswered_count=attempt.unanswered_count,
            total_marks=total_possible,
            score=attempt.score,
            percentage=attempt.percentage,
            accuracy=attempt.accuracy,
            time_taken_seconds=attempt.time_taken_seconds,
            passed=attempt.passed,
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

    def _update_topic_performance(self, user_id: str, topic_id: int, attempted_delta: int, correct_delta: int) -> None:
        """Internal helper updating StudentTopicPerformance metrics."""
        if attempted_delta <= 0:
            return
        perf = self.db.scalar(
            select(StudentTopicPerformance).where(
                StudentTopicPerformance.user_id == user_id,
                StudentTopicPerformance.topic_id == topic_id,
            )
        )
        if not perf:
            accuracy = (correct_delta / attempted_delta) * 100.0 if attempted_delta > 0 else 0.0
            weakness = round(100.0 - accuracy, 2)
            perf = StudentTopicPerformance(
                user_id=user_id,
                topic_id=topic_id,
                total_questions_attempted=attempted_delta,
                correct_attempts=correct_delta,
                weakness_score=weakness,
            )
            self.db.add(perf)
        else:
            perf.total_questions_attempted += attempted_delta
            perf.correct_attempts += correct_delta
            overall_acc = (perf.correct_attempts / perf.total_questions_attempted) * 100.0 if perf.total_questions_attempted > 0 else 0.0
            perf.weakness_score = round(100.0 - overall_acc, 2)
            perf.last_updated = datetime.now(timezone.utc)
