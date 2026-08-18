from datetime import datetime, timezone
from typing import List, Optional, Tuple

from sqlalchemy.orm import Session

from backend.app.core.exceptions import ForbiddenException, NotFoundException, ValidationException
from backend.app.models.quiz import Quiz, QuizQuestion
from backend.app.models.user import User
from backend.app.repositories.content_repository import QuestionRepository
from backend.app.repositories.quiz_repository import QuizRepository
from backend.app.schemas.quiz import QuestionPoolInfoResponse, QuizCreate, QuizUpdate
from backend.app.services.base import BaseService
from backend.app.services.question_selection_service import QuestionSelectionService


class QuizService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db)
        self.quiz_repo = QuizRepository()
        self.question_repo = QuestionRepository()
        self.selection_service = QuestionSelectionService(db)

    def get_quizzes(
        self,
        exam_id: Optional[int] = None,
        subject_id: Optional[int] = None,
        topic_id: Optional[int] = None,
        quiz_type: Optional[str] = None,
        status: Optional[str] = None,
        is_published: Optional[bool] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[Quiz], int]:
        return self.quiz_repo.get_multi_filtered(
            self.db,
            exam_id=exam_id,
            subject_id=subject_id,
            topic_id=topic_id,
            quiz_type=quiz_type,
            status=status,
            is_published=is_published,
            search=search,
            skip=skip,
            limit=limit,
        )

    def get_quiz(self, quiz_id: int) -> Quiz:
        quiz = self.quiz_repo.get_with_questions(self.db, quiz_id=quiz_id)
        if not quiz:
            raise NotFoundException(message=f"Quiz with ID {quiz_id} not found.")
        return quiz

    def create_quiz(self, obj_in: QuizCreate, creator_id: Optional[str] = None) -> Quiz:
        def _action():
            questions_input = obj_in.questions or []
            quiz_data = obj_in.model_dump(exclude={"questions"})
            quiz_data["created_by"] = creator_id
            if quiz_data.get("is_published"):
                quiz_data["status"] = "PUBLISHED"

            quiz = self.quiz_repo.create(self.db, obj_in=quiz_data)

            total_marks = 0.0
            for idx, q_item in enumerate(questions_input):
                q = self.question_repo.get(self.db, id=q_item.question_id)
                if not q:
                    raise NotFoundException(message=f"Question with ID '{q_item.question_id}' not found.")
                assoc = QuizQuestion(
                    quiz_id=quiz.id,
                    question_id=q_item.question_id,
                    sort_order=q_item.sort_order if q_item.sort_order != 0 else idx + 1,
                    marks=q_item.marks,
                    negative_marks=q_item.negative_marks,
                )
                self.db.add(assoc)
                total_marks += q_item.marks

            quiz.question_count = len(questions_input)
            if total_marks > 0:
                quiz.total_marks = total_marks

            self.db.flush()
            return quiz

        return self.execute_in_transaction(_action)

    def update_quiz(self, quiz_id: int, obj_in: QuizUpdate) -> Quiz:
        def _action():
            quiz = self.get_quiz(quiz_id)
            update_data = obj_in.model_dump(exclude_unset=True)
            if "is_published" in update_data:
                update_data["status"] = "PUBLISHED" if update_data["is_published"] else "DRAFT"

            return self.quiz_repo.update(self.db, db_obj=quiz, obj_in=update_data)

        return self.execute_in_transaction(_action)

    def publish_quiz(self, quiz_id: int) -> Quiz:
        def _action():
            quiz = self.get_quiz(quiz_id)
            # Validate question pool before publication if no static question associations
            if not quiz.question_associations:
                req_count = quiz.question_count if quiz.question_count > 0 else 10
                pool = self.selection_service.get_published_questions_pool(
                    exam_id=quiz.exam_id,
                    subject_id=quiz.subject_id,
                    topic_id=quiz.topic_id,
                )
                if len(pool) < req_count:
                    raise ValidationException(
                        message=f"Cannot publish quiz: Requested question count is {req_count}, but only {len(pool)} published questions exist in database for this taxonomy scope."
                    )

            quiz.status = "PUBLISHED"
            quiz.is_published = True
            quiz.updated_at = datetime.now(timezone.utc)
            self.db.flush()
            return quiz

        return self.execute_in_transaction(_action)

    def archive_quiz(self, quiz_id: int) -> Quiz:
        def _action():
            quiz = self.get_quiz(quiz_id)
            quiz.status = "ARCHIVED"
            quiz.is_published = False
            quiz.updated_at = datetime.now(timezone.utc)
            self.db.flush()
            return quiz

        return self.execute_in_transaction(_action)

    def delete_quiz(self, quiz_id: int) -> None:
        def _action():
            quiz = self.get_quiz(quiz_id)
            if quiz.attempts:
                raise ValidationException(
                    message=f"Cannot delete quiz '{quiz.title}' because it contains {len(quiz.attempts)} attempt records. Archive it instead to preserve historical results."
                )
            self.quiz_repo.remove(self.db, id=quiz_id)

        self.execute_in_transaction(_action)

    def inspect_question_pool(self, quiz_id: int) -> QuestionPoolInfoResponse:
        quiz = self.get_quiz(quiz_id)
        req_count = quiz.question_count if quiz.question_count > 0 else (len(quiz.question_associations) or 10)
        pool = self.selection_service.get_published_questions_pool(
            exam_id=quiz.exam_id,
            subject_id=quiz.subject_id,
            topic_id=quiz.topic_id,
        )
        avail_count = len(pool)
        return QuestionPoolInfoResponse(
            quiz_id=quiz.id,
            exam_id=quiz.exam_id,
            subject_id=quiz.subject_id,
            topic_id=quiz.topic_id,
            requested_count=req_count,
            available_published_questions=avail_count,
            has_sufficient_pool=avail_count >= req_count,
            details={
                "static_associations_count": len(quiz.question_associations),
                "randomized_selection": quiz.randomize_questions,
            },
        )
