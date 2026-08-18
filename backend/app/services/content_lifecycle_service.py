from typing import Any, Dict, List, Optional, Set

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.core.exceptions import BadRequestException, NotFoundException, ValidationException
from backend.app.models.content import Exam, Question, Subject, Topic
from backend.app.models.material import StudyMaterial
from backend.app.services.base import BaseService


class ContentLifecycleService(BaseService):
    """
    Centralized Content Lifecycle & Visibility Engine.
    Enforces status state transitions and student-facing content visibility policies.
    """

    TAXONOMY_STATUSES = {"DRAFT", "ACTIVE", "INACTIVE", "ARCHIVED"}
    CONTENT_STATUSES = {"DRAFT", "REVIEW", "PUBLISHED", "UNPUBLISHED", "ARCHIVED"}

    ALLOWED_TAXONOMY_TRANSITIONS = {
        "DRAFT": {"ACTIVE", "ARCHIVED"},
        "ACTIVE": {"INACTIVE", "ARCHIVED"},
        "INACTIVE": {"ACTIVE", "ARCHIVED"},
        "ARCHIVED": {"ACTIVE", "INACTIVE"},
    }

    ALLOWED_CONTENT_TRANSITIONS = {
        "DRAFT": {"REVIEW", "PUBLISHED", "ARCHIVED"},
        "REVIEW": {"DRAFT", "PUBLISHED", "ARCHIVED"},
        "PUBLISHED": {"UNPUBLISHED", "ARCHIVED"},
        "UNPUBLISHED": {"PUBLISHED", "ARCHIVED"},
        "ARCHIVED": {"DRAFT", "REVIEW", "UNPUBLISHED"},
    }

    def validate_taxonomy_transition(self, current_status: str, target_status: str) -> None:
        target_upper = target_status.upper()
        if target_upper not in self.TAXONOMY_STATUSES:
            raise ValidationException(
                message=f"Invalid taxonomy status '{target_status}'. Must be one of {self.TAXONOMY_STATUSES}."
            )
        if current_status != target_upper:
            allowed = self.ALLOWED_TAXONOMY_TRANSITIONS.get(current_status, set())
            if target_upper not in allowed:
                raise BadRequestException(
                    message=f"Invalid status transition from '{current_status}' to '{target_upper}'. Allowed: {allowed}"
                )

    def validate_content_transition(self, current_status: str, target_status: str) -> None:
        target_upper = target_status.upper()
        if target_upper not in self.CONTENT_STATUSES:
            raise ValidationException(
                message=f"Invalid content status '{target_status}'. Must be one of {self.CONTENT_STATUSES}."
            )
        if current_status != target_upper:
            allowed = self.ALLOWED_CONTENT_TRANSITIONS.get(current_status, set())
            if target_upper not in allowed:
                raise BadRequestException(
                    message=f"Invalid status transition from '{current_status}' to '{target_upper}'. Allowed: {allowed}"
                )

    def validate_question_for_publish(self, question: Question) -> None:
        """
        Validates question completeness before transitioning to PUBLISHED status.
        """
        errors: List[str] = []
        if not question.question_text or not question.question_text.strip():
            errors.append("Question text cannot be empty.")
        if not question.type or question.type.upper() not in ("MCQ", "MSQ", "NAT"):
            errors.append(f"Invalid question type '{question.type}'.")
        if not question.correct_answer or not question.correct_answer.strip():
            errors.append("Correct answer key is missing.")
        if question.type.upper() in ("MCQ", "MSQ"):
            if not question.options or len(question.options) < 2:
                errors.append("MCQ/MSQ question requires at least 2 options.")
        if not question.topic_id:
            errors.append("Question must belong to a valid topic.")

        if errors:
            raise ValidationException(message=f"Cannot publish malformed question: {'; '.join(errors)}")

    # --- Publishing Actions ---
    def publish_question(self, question_id: str, user_id: Optional[str] = None) -> Question:
        def _action():
            question = self.db.get(Question, question_id)
            if not question:
                raise NotFoundException(message=f"Question with ID '{question_id}' not found.")
            self.validate_content_transition(question.status, "PUBLISHED")
            self.validate_question_for_publish(question)
            question.status = "PUBLISHED"
            if user_id:
                question.updated_by = user_id
            return question

        return self.execute_in_transaction(_action)

    def unpublish_question(self, question_id: str, user_id: Optional[str] = None) -> Question:
        def _action():
            question = self.db.get(Question, question_id)
            if not question:
                raise NotFoundException(message=f"Question with ID '{question_id}' not found.")
            self.validate_content_transition(question.status, "UNPUBLISHED")
            question.status = "UNPUBLISHED"
            if user_id:
                question.updated_by = user_id
            return question

        return self.execute_in_transaction(_action)

    def archive_question(self, question_id: str, user_id: Optional[str] = None) -> Question:
        def _action():
            question = self.db.get(Question, question_id)
            if not question:
                raise NotFoundException(message=f"Question with ID '{question_id}' not found.")
            self.validate_content_transition(question.status, "ARCHIVED")
            question.status = "ARCHIVED"
            if user_id:
                question.updated_by = user_id
            return question

        return self.execute_in_transaction(_action)

    def bulk_update_question_status(
        self, question_ids: List[str], target_status: str, user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        def _action():
            target_upper = target_status.upper()
            updated_count = 0
            skipped_count = 0
            for q_id in question_ids:
                q = self.db.get(Question, q_id)
                if not q:
                    skipped_count += 1
                    continue
                try:
                    self.validate_content_transition(q.status, target_upper)
                    if target_upper == "PUBLISHED":
                        self.validate_question_for_publish(q)
                    q.status = target_upper
                    if user_id:
                        q.updated_by = user_id
                    updated_count += 1
                except Exception:
                    skipped_count += 1

            return {"total_requested": len(question_ids), "updated": updated_count, "skipped": skipped_count}

        return self.execute_in_transaction(_action)
