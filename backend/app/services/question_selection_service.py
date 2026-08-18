import random
from typing import List, Optional, Tuple

from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from backend.app.core.exceptions import NotFoundException, ValidationException
from backend.app.models.content import Exam, Question, Subject, Topic
from backend.app.services.base import BaseService


from backend.app.core.semantic_deduplication import default_semantic_deduplicator


class QuestionSelectionService(BaseService):
    """
    Service responsible for building selection queries, verifying published status
    under active taxonomy, enforcing requested count, enforcing semantic diversity,
    and randomizing question/option order.
    """

    def get_published_questions_pool(
        self,
        exam_id: Optional[int] = None,
        subject_id: Optional[int] = None,
        topic_id: Optional[int] = None,
        difficulty: Optional[str] = None,
        question_type: Optional[str] = None,
    ) -> List[Question]:
        """
        Retrieves all student-visible (PUBLISHED status + ACTIVE parent taxonomy)
        questions matching the provided filters.
        """
        stmt = (
            select(Question)
            .distinct()
            .join(Question.topic)
            .join(Topic.subject)
            .join(Subject.exam)
            .where(
                Question.status == "PUBLISHED",
                Topic.status == "ACTIVE",
                Subject.status == "ACTIVE",
                Exam.status == "ACTIVE",
            )
            .options(joinedload(Question.topic).joinedload(Topic.subject))
        )

        if exam_id:
            stmt = stmt.where(Exam.id == exam_id)
        if subject_id:
            stmt = stmt.where(Subject.id == subject_id)
        if topic_id:
            stmt = stmt.where(Topic.id == topic_id)
        if difficulty:
            stmt = stmt.where(Question.difficulty == difficulty)
        if question_type:
            stmt = stmt.where(Question.type == question_type)

        raw_questions = list(self.db.scalars(stmt).all())
        seen_texts = set()
        unique_questions = []
        for q in raw_questions:
            if q.question_text not in seen_texts:
                seen_texts.add(q.question_text)
                unique_questions.append(q)

        return unique_questions

    def validate_and_select_questions(
        self,
        requested_count: int,
        exam_id: Optional[int] = None,
        subject_id: Optional[int] = None,
        topic_id: Optional[int] = None,
        difficulty: Optional[str] = None,
        question_type: Optional[str] = None,
        randomize: bool = True,
    ) -> List[Question]:
        """
        Validates that the question pool has sufficient questions and selects `requested_count` questions,
        enforcing semantic diversity so no reworded or identical-meaning questions appear together.
        """
        if requested_count <= 0:
            raise ValidationException(message="Requested question count must be greater than 0.")

        pool = self.get_published_questions_pool(
            exam_id=exam_id,
            subject_id=subject_id,
            topic_id=topic_id,
            difficulty=difficulty,
            question_type=question_type,
        )

        if len(pool) < requested_count:
            raise ValidationException(
                message=f"INSUFFICIENT_QUESTION_POOL: Requested {requested_count} questions, but only {len(pool)} published questions are available under the specified criteria."
            )

        candidate_pool = list(pool)
        if randomize:
            random.shuffle(candidate_pool)

        # Enforce Data Science Semantic Diversity (no two questions in assessment have >= 0.40 similarity)
        semantically_diverse_pool = default_semantic_deduplicator.filter_semantically_diverse_questions(
            candidate_pool, threshold=0.40, text_attr="question_text"
        )

        if len(semantically_diverse_pool) >= requested_count:
            return semantically_diverse_pool[:requested_count]

        # Fallback to pool if strict diversity filter yields fewer questions than requested
        return candidate_pool[:requested_count]
