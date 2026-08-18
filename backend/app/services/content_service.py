from typing import List, Optional, Tuple

from sqlalchemy.orm import Session

from backend.app.core.exceptions import BadRequestException, ConflictException, NotFoundException
from backend.app.models.content import Exam, ExamCategory, Question, Subject, Subtopic, Topic
from backend.app.repositories.content_repository import (
    ExamCategoryRepository,
    ExamRepository,
    QuestionRepository,
    SubjectRepository,
    SubtopicRepository,
    TopicRepository,
)
from backend.app.schemas.content import (
    ExamCategoryCreate,
    ExamCategoryUpdate,
    ExamCreate,
    ExamUpdate,
    QuestionCreate,
    QuestionUpdate,
    SubjectCreate,
    SubjectUpdate,
    SubtopicCreate,
    SubtopicUpdate,
    TopicCreate,
    TopicUpdate,
)
from backend.app.services.base import BaseService


class ContentService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db)
        self.category_repo = ExamCategoryRepository()
        self.exam_repo = ExamRepository()
        self.subject_repo = SubjectRepository()
        self.topic_repo = TopicRepository()
        self.subtopic_repo = SubtopicRepository()
        self.question_repo = QuestionRepository()

    # --- Exam Categories ---
    def get_categories(self) -> List[ExamCategory]:
        return self.category_repo.get_multi(self.db)

    def create_category(self, obj_in: ExamCategoryCreate) -> ExamCategory:
        def _action():
            return self.category_repo.create(self.db, obj_in=obj_in)

        return self.execute_in_transaction(_action)

    # --- Exams ---
    def get_exams(
        self,
        category_id: Optional[int] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Exam]:
        return self.exam_repo.get_multi_by_category(self.db, category_id=category_id, status=status, skip=skip, limit=limit)

    def get_exam(self, exam_id: int) -> Exam:
        exam = self.exam_repo.get(self.db, id=exam_id)
        if not exam:
            raise NotFoundException(message=f"Exam with ID {exam_id} not found.")
        return exam

    def create_exam(self, obj_in: ExamCreate) -> Exam:
        def _action():
            if self.exam_repo.get_by_code(self.db, code=obj_in.code):
                raise ConflictException(message=f"Exam code '{obj_in.code}' already exists.")
            return self.exam_repo.create(self.db, obj_in=obj_in)

        return self.execute_in_transaction(_action)

    def update_exam(self, exam_id: int, obj_in: ExamUpdate) -> Exam:
        def _action():
            exam = self.get_exam(exam_id)
            if obj_in.code and obj_in.code != exam.code:
                if self.exam_repo.get_by_code(self.db, code=obj_in.code):
                    raise ConflictException(message=f"Exam code '{obj_in.code}' already exists.")
            return self.exam_repo.update(self.db, db_obj=exam, obj_in=obj_in)

        return self.execute_in_transaction(_action)

    def delete_exam(self, exam_id: int) -> None:
        def _action():
            exam = self.get_exam(exam_id)
            if exam.subjects:
                raise BadRequestException(
                    message=f"Cannot delete exam '{exam.name}' because it contains {len(exam.subjects)} active subjects. Deactivate or archive it instead."
                )
            self.exam_repo.remove(self.db, id=exam_id)

        self.execute_in_transaction(_action)

    # --- Subjects ---
    def get_subjects(
        self,
        exam_id: Optional[int] = None,
        status: Optional[str] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[Subject], int]:
        return self.subject_repo.get_multi_filtered(
            self.db, exam_id=exam_id, status=status, search=search, skip=skip, limit=limit
        )

    def get_subject(self, subject_id: int) -> Subject:
        subject = self.subject_repo.get(self.db, id=subject_id)
        if not subject:
            raise NotFoundException(message=f"Subject with ID {subject_id} not found.")
        return subject

    def create_subject(self, obj_in: SubjectCreate) -> Subject:
        def _action():
            self.get_exam(obj_in.exam_id)
            if self.subject_repo.get_by_exam_and_code(self.db, exam_id=obj_in.exam_id, code=obj_in.code):
                raise ConflictException(message=f"Subject code '{obj_in.code}' already exists for exam ID {obj_in.exam_id}.")
            return self.subject_repo.create(self.db, obj_in=obj_in)

        return self.execute_in_transaction(_action)

    def update_subject(self, subject_id: int, obj_in: SubjectUpdate) -> Subject:
        def _action():
            subject = self.get_subject(subject_id)
            if obj_in.code:
                norm_code = obj_in.code.strip().upper()
                existing = self.subject_repo.get_by_exam_and_code(self.db, exam_id=subject.exam_id, code=norm_code)
                if existing and existing.id != subject_id:
                    raise ConflictException(message=f"Subject code '{norm_code}' already exists for this exam.")
            return self.subject_repo.update(self.db, db_obj=subject, obj_in=obj_in)

        return self.execute_in_transaction(_action)

    def delete_subject(self, subject_id: int) -> None:
        def _action():
            subject = self.get_subject(subject_id)
            if subject.topics:
                raise BadRequestException(
                    message=f"Cannot delete subject '{subject.name}' because it contains {len(subject.topics)} topics. Deactivate or archive it instead."
                )
            self.subject_repo.remove(self.db, id=subject_id)

        self.execute_in_transaction(_action)

    # --- Topics & Subtopics ---
    def get_topics(
        self,
        subject_id: Optional[int] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[Topic], int]:
        return self.topic_repo.get_multi_by_subject(self.db, subject_id=subject_id, status=status, skip=skip, limit=limit)

    def get_topic(self, topic_id: int) -> Topic:
        topic = self.topic_repo.get(self.db, id=topic_id)
        if not topic:
            raise NotFoundException(message=f"Topic with ID {topic_id} not found.")
        return topic

    def create_topic(self, obj_in: TopicCreate) -> Topic:
        def _action():
            self.get_subject(obj_in.subject_id)
            norm_name = obj_in.name.strip()
            if self.topic_repo.get_by_subject_and_name(self.db, subject_id=obj_in.subject_id, name=norm_name):
                raise ConflictException(message=f"Topic '{norm_name}' already exists under this subject.")
            return self.topic_repo.create(self.db, obj_in=obj_in)

        return self.execute_in_transaction(_action)

    def update_topic(self, topic_id: int, obj_in: TopicUpdate) -> Topic:
        def _action():
            topic = self.get_topic(topic_id)
            if obj_in.name:
                norm_name = obj_in.name.strip()
                existing = self.topic_repo.get_by_subject_and_name(self.db, subject_id=topic.subject_id, name=norm_name)
                if existing and existing.id != topic_id:
                    raise ConflictException(message=f"Topic '{norm_name}' already exists under this subject.")
            return self.topic_repo.update(self.db, db_obj=topic, obj_in=obj_in)

        return self.execute_in_transaction(_action)

    def delete_topic(self, topic_id: int) -> None:
        def _action():
            topic = self.get_topic(topic_id)
            if topic.questions:
                raise BadRequestException(
                    message=f"Cannot delete topic '{topic.name}' because it contains {len(topic.questions)} questions. Archive or deactivate it instead."
                )
            self.topic_repo.remove(self.db, id=topic_id)

        self.execute_in_transaction(_action)

    def get_subtopics(self, topic_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[Subtopic]:
        return self.subtopic_repo.get_multi_by_topic(self.db, topic_id=topic_id, skip=skip, limit=limit)

    def create_subtopic(self, obj_in: SubtopicCreate) -> Subtopic:
        def _action():
            self.get_topic(obj_in.topic_id)
            return self.subtopic_repo.create(self.db, obj_in=obj_in)

        return self.execute_in_transaction(_action)

    # --- Questions ---
    def get_questions(
        self,
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
        return self.question_repo.get_multi_filtered(
            self.db,
            topic_id=topic_id,
            subtopic_id=subtopic_id,
            difficulty=difficulty,
            question_type=question_type,
            status=status,
            student_visible_only=student_visible_only,
            search=search,
            skip=skip,
            limit=limit,
        )

    def get_question(self, question_id: str) -> Question:
        question = self.question_repo.get(self.db, id=question_id)
        if not question:
            raise NotFoundException(message=f"Question with ID {question_id} not found.")
        return question

    def create_question(self, obj_in: QuestionCreate, user_id: Optional[str] = None) -> Question:
        def _action():
            if self.question_repo.get(self.db, id=obj_in.id):
                raise ConflictException(message=f"Question with ID '{obj_in.id}' already exists.")
            data = obj_in.model_dump()
            if user_id:
                data["created_by"] = user_id
                data["updated_by"] = user_id
            q_obj = Question(**data)
            self.db.add(q_obj)
            return q_obj

        return self.execute_in_transaction(_action)

    def update_question(self, question_id: str, obj_in: QuestionUpdate, user_id: Optional[str] = None) -> Question:
        def _action():
            question = self.get_question(question_id)
            data = obj_in.model_dump(exclude_unset=True)
            if user_id:
                data["updated_by"] = user_id
            for k, v in data.items():
                setattr(question, k, v)
            return question

        return self.execute_in_transaction(_action)

    def delete_question(self, question_id: str) -> None:
        def _action():
            question = self.get_question(question_id)
            if question.quiz_associations:
                raise BadRequestException(
                    message=f"Cannot delete question '{question_id}' because it is associated with quizzes. Unpublish or archive it instead."
                )
            self.question_repo.remove(self.db, id=question_id)

        self.execute_in_transaction(_action)
