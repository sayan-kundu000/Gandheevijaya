from typing import List, Optional, Tuple

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, selectinload

from backend.app.models.content import Exam, ExamCategory, Question, Subject, Subtopic, Topic
from backend.app.repositories.base import BaseRepository


class ExamCategoryRepository(BaseRepository[ExamCategory]):
    def __init__(self):
        super().__init__(ExamCategory)


class ExamRepository(BaseRepository[Exam]):
    def __init__(self):
        super().__init__(Exam)

    def get_by_code(self, db: Session, code: str) -> Optional[Exam]:
        return db.scalar(select(Exam).where(func.upper(Exam.code) == code.strip().upper()))

    def get_multi_by_category(
        self,
        db: Session,
        category_id: Optional[int] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Exam]:
        stmt = select(Exam).options(selectinload(Exam.category))
        if category_id is not None:
            stmt = stmt.where(Exam.category_id == category_id)
        if status is not None:
            stmt = stmt.where(Exam.status == status)
        stmt = stmt.order_by(Exam.display_order.asc(), Exam.name.asc()).offset(skip).limit(limit)
        return list(db.scalars(stmt).all())


class SubjectRepository(BaseRepository[Subject]):
    def __init__(self):
        super().__init__(Subject)

    def get_by_exam_and_code(self, db: Session, exam_id: int, code: str) -> Optional[Subject]:
        return db.scalar(
            select(Subject).where(Subject.exam_id == exam_id, func.upper(Subject.code) == code.strip().upper())
        )

    def get_multi_filtered(
        self,
        db: Session,
        exam_id: Optional[int] = None,
        status: Optional[str] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[Subject], int]:
        stmt = select(Subject).options(selectinload(Subject.exam))
        if exam_id is not None:
            stmt = stmt.where(Subject.exam_id == exam_id)
        if status is not None:
            stmt = stmt.where(Subject.status == status)
        if search:
            search_pattern = f"%{search}%"
            stmt = stmt.where(or_(Subject.name.ilike(search_pattern), Subject.code.ilike(search_pattern)))

        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = db.scalar(count_stmt) or 0

        stmt = stmt.order_by(Subject.display_order.asc(), Subject.name.asc()).offset(skip).limit(limit)
        items = list(db.scalars(stmt).all())
        return items, total


class TopicRepository(BaseRepository[Topic]):
    def __init__(self):
        super().__init__(Topic)

    def get_by_subject_and_name(self, db: Session, subject_id: int, name: str) -> Optional[Topic]:
        return db.scalar(
            select(Topic).where(Topic.subject_id == subject_id, func.lower(Topic.name) == name.strip().lower())
        )

    def get_multi_by_subject(
        self,
        db: Session,
        subject_id: Optional[int] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[Topic], int]:
        stmt = select(Topic).options(selectinload(Topic.subtopics), selectinload(Topic.subject))
        if subject_id is not None:
            stmt = stmt.where(Topic.subject_id == subject_id)
        if status is not None:
            stmt = stmt.where(Topic.status == status)

        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = db.scalar(count_stmt) or 0

        stmt = stmt.order_by(Topic.display_order.asc(), Topic.name.asc()).offset(skip).limit(limit)
        items = list(db.scalars(stmt).all())
        return items, total


class SubtopicRepository(BaseRepository[Subtopic]):
    def __init__(self):
        super().__init__(Subtopic)

    def get_multi_by_topic(
        self, db: Session, topic_id: Optional[int] = None, skip: int = 0, limit: int = 100
    ) -> List[Subtopic]:
        stmt = select(Subtopic)
        if topic_id is not None:
            stmt = stmt.where(Subtopic.topic_id == topic_id)
        stmt = stmt.offset(skip).limit(limit)
        return list(db.scalars(stmt).all())


class QuestionRepository(BaseRepository[Question]):
    def __init__(self):
        super().__init__(Question)

    def get_multi_filtered(
        self,
        db: Session,
        topic_id: Optional[int] = None,
        subtopic_id: Optional[int] = None,
        difficulty: Optional[str] = None,
        question_type: Optional[str] = None,
        status: Optional[str] = None,
        student_visible_only: bool = False,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[Question], int]:
        stmt = select(Question).options(selectinload(Question.topic), selectinload(Question.subtopic))

        if student_visible_only:
            # Enforce Student Content Visibility Policy:
            # Question PUBLISHED AND Topic ACTIVE AND Subject ACTIVE AND Exam ACTIVE
            stmt = (
                stmt.join(Question.topic)
                .join(Topic.subject)
                .join(Subject.exam)
                .where(
                    Question.status == "PUBLISHED",
                    Topic.status == "ACTIVE",
                    Subject.status == "ACTIVE",
                    Exam.status == "ACTIVE",
                )
            )
        elif status is not None:
            stmt = stmt.where(Question.status == status)

        if topic_id is not None:
            stmt = stmt.where(Question.topic_id == topic_id)
        if subtopic_id is not None:
            stmt = stmt.where(Question.subtopic_id == subtopic_id)
        if difficulty:
            stmt = stmt.where(Question.difficulty == difficulty)
        if question_type:
            stmt = stmt.where(Question.type == question_type)
        if search:
            search_pattern = f"%{search}%"
            stmt = stmt.where(Question.question_text.ilike(search_pattern))

        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = db.scalar(count_stmt) or 0

        stmt = stmt.order_by(Question.id.asc()).offset(skip).limit(limit)
        items = list(db.scalars(stmt).all())
        return items, total
