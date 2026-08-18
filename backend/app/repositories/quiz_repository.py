from typing import List, Optional, Tuple

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from backend.app.models.attempt import Attempt, AttemptAnswer
from backend.app.models.quiz import Quiz, QuizQuestion
from backend.app.repositories.base import BaseRepository


class QuizRepository(BaseRepository[Quiz]):
    def __init__(self):
        super().__init__(Quiz)

    def get_with_questions(self, db: Session, quiz_id: int) -> Optional[Quiz]:
        stmt = (
            select(Quiz)
            .options(
                selectinload(Quiz.exam),
                selectinload(Quiz.subject),
                selectinload(Quiz.topic),
                selectinload(Quiz.question_associations).selectinload(QuizQuestion.question),
            )
            .where(Quiz.id == quiz_id)
        )
        return db.scalar(stmt)

    def get_multi_filtered(
        self,
        db: Session,
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
        stmt = select(Quiz).options(
            selectinload(Quiz.exam),
            selectinload(Quiz.subject),
            selectinload(Quiz.topic),
        )

        if exam_id is not None:
            stmt = stmt.where(Quiz.exam_id == exam_id)
        if subject_id is not None:
            stmt = stmt.where(Quiz.subject_id == subject_id)
        if topic_id is not None:
            stmt = stmt.where(Quiz.topic_id == topic_id)
        if quiz_type:
            stmt = stmt.where(Quiz.quiz_type == quiz_type)
        if status:
            stmt = stmt.where(Quiz.status == status)
        if is_published is not None:
            stmt = stmt.where(Quiz.is_published == is_published)
        if search:
            stmt = stmt.where(Quiz.title.ilike(f"%{search}%"))

        stmt = stmt.order_by(Quiz.created_at.desc())

        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = db.scalar(count_stmt) or 0

        stmt = stmt.offset(skip).limit(limit)
        items = list(db.scalars(stmt).all())
        return items, total


class AttemptRepository(BaseRepository[Attempt]):
    def __init__(self):
        super().__init__(Attempt)

    def get_with_details(self, db: Session, attempt_id: str) -> Optional[Attempt]:
        stmt = (
            select(Attempt)
            .options(
                selectinload(Attempt.quiz).selectinload(Quiz.subject),
                selectinload(Attempt.answers).selectinload(AttemptAnswer.question),
            )
            .where(Attempt.id == attempt_id)
        )
        return db.scalar(stmt)

    def get_multi_filtered(
        self,
        db: Session,
        user_id: Optional[str] = None,
        quiz_id: Optional[int] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[Attempt], int]:
        stmt = select(Attempt).options(selectinload(Attempt.quiz))

        if user_id:
            stmt = stmt.where(Attempt.user_id == user_id)
        if quiz_id is not None:
            stmt = stmt.where(Attempt.quiz_id == quiz_id)
        if status:
            stmt = stmt.where(Attempt.status == status)

        stmt = stmt.order_by(Attempt.started_at.desc())

        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = db.scalar(count_stmt) or 0

        stmt = stmt.offset(skip).limit(limit)
        items = list(db.scalars(stmt).all())
        return items, total


class AttemptAnswerRepository(BaseRepository[AttemptAnswer]):
    def __init__(self):
        super().__init__(AttemptAnswer)
