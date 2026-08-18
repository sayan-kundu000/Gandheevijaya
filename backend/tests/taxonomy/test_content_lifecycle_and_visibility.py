import uuid
import pytest
from sqlalchemy.orm import Session

from backend.app.core.exceptions import BadRequestException, ValidationException
from backend.app.models.content import Exam, ExamCategory, Question, Subject, Topic
from backend.app.services.content_lifecycle_service import ContentLifecycleService
from backend.app.services.content_service import ContentService


def test_content_lifecycle_transitions_and_student_visibility(db_session: Session):
    service = ContentService(db_session)
    lc_service = ContentLifecycleService(db_session)

    # 1. Setup Taxonomy
    cat = ExamCategory(name="GATE CS", slug=f"g-{uuid.uuid4().hex[:6]}")
    db_session.add(cat)
    db_session.flush()

    exam = Exam(category_id=cat.id, name="GATE Computer Science", code=f"GCS_{uuid.uuid4().hex[:6]}", status="ACTIVE")
    db_session.add(exam)
    db_session.flush()

    subj = Subject(exam_id=exam.id, name="Data Structures", code=f"DS_{uuid.uuid4().hex[:6]}", status="ACTIVE")
    db_session.add(subj)
    db_session.flush()

    topic = Topic(subject_id=subj.id, name="Trees", status="ACTIVE")
    db_session.add(topic)
    db_session.flush()

    # 2. Create Question in DRAFT status
    q_id = f"Q-LC-{uuid.uuid4().hex[:6]}"
    q = Question(
        id=q_id,
        topic_id=topic.id,
        difficulty="easy",
        type="MCQ",
        question_text="What is root node in a tree?",
        options=["Top node", "Leaf node"],
        correct_answer="Top node",
        explanation="Top node of tree is root.",
        status="DRAFT",
    )
    db_session.add(q)
    db_session.commit()

    # 3. Student Visibility Filter -> DRAFT question must NOT be visible!
    qs_student, total_student = service.get_questions(topic_id=topic.id, student_visible_only=True)
    assert q_id not in [x.id for x in qs_student]

    # 4. Admin publishes question -> Now visible!
    published_q = lc_service.publish_question(q_id)
    assert published_q.status == "PUBLISHED"

    qs_student_published, _ = service.get_questions(topic_id=topic.id, student_visible_only=True)
    assert q_id in [x.id for x in qs_student_published]

    # 5. Inactivate Topic -> Question automatically hidden from students!
    topic.status = "INACTIVE"
    db_session.commit()

    qs_student_after_inactive, _ = service.get_questions(topic_id=topic.id, student_visible_only=True)
    assert q_id not in [x.id for x in qs_student_after_inactive]
