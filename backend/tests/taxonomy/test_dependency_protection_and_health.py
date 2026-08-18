import uuid
import pytest
from sqlalchemy.orm import Session

from backend.app.core.exceptions import BadRequestException
from backend.app.models.content import Exam, ExamCategory, Question, Subject, Topic
from backend.app.services.content_service import ContentService
from backend.app.services.taxonomy_service import TaxonomyService


def test_dependency_protection_and_content_health(db_session: Session):
    service = ContentService(db_session)
    tax_service = TaxonomyService(db_session)

    # Setup taxonomy with active question
    cat = ExamCategory(name="Test Category", slug=f"t-{uuid.uuid4().hex[:6]}")
    db_session.add(cat)
    db_session.flush()

    exam = Exam(category_id=cat.id, name="Test Exam", code=f"TE_{uuid.uuid4().hex[:6]}")
    db_session.add(exam)
    db_session.flush()

    subj = Subject(exam_id=exam.id, name="Test Subject", code=f"TS_{uuid.uuid4().hex[:6]}")
    db_session.add(subj)
    db_session.flush()

    topic = Topic(subject_id=subj.id, name="Test Topic")
    db_session.add(topic)
    db_session.flush()

    q_id = f"Q-DEP-{uuid.uuid4().hex[:6]}"
    q = Question(
        id=q_id,
        topic_id=topic.id,
        difficulty="easy",
        type="MCQ",
        question_text="Sample Test Question",
        options=["A", "B"],
        correct_answer="A",
        explanation="Explanation text",
        status="PUBLISHED",
    )
    db_session.add(q)
    db_session.commit()

    # Attempting to delete topic with active question must raise BadRequestException
    with pytest.raises(BadRequestException):
        service.delete_topic(topic.id)

    # Attempting to delete subject with active topic must raise BadRequestException
    with pytest.raises(BadRequestException):
        service.delete_subject(subj.id)

    # Verify Health Report Runs Cleanly
    health = tax_service.get_content_health_report()
    assert health.total_exams >= 1
    assert health.total_questions >= 1
