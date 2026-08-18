import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.app.models.content import Exam, ExamCategory, Subject, Topic
from backend.tests.helpers import get_admin_auth_headers


def test_xss_payload_safety(client: TestClient, db_session: Session):
    """
    SECURITY TEST: Verify XSS injection vectors (<script>alert(1)</script>)
    are safely stored and returned without unsafe execution or server crashes.
    """
    headers = get_admin_auth_headers(db_session)

    # Create Taxonomy hierarchy
    cat = ExamCategory(name="CS Cat", slug="cs-cat-xss")
    db_session.add(cat)
    db_session.flush()

    exam = Exam(category_id=cat.id, name="XSS Exam", code="XSS_EXAM", status="ACTIVE")
    db_session.add(exam)
    db_session.flush()

    subject = Subject(exam_id=exam.id, name="XSS Subject", code="XSS_SUB", status="ACTIVE")
    db_session.add(subject)
    db_session.flush()

    topic = Topic(subject_id=subject.id, name="XSS Topic", code="XSS_TOP", status="ACTIVE")
    db_session.add(topic)
    db_session.commit()

    # Post question with script injection payload
    xss_payload = "<script>alert('xss-exploit')</script><img src=x onerror=alert(1)>"
    res = client.post(
        "/api/v1/admin/questions",
        json={
            "id": "Q-XSS-TEST-001",
            "topic_id": topic.id,
            "type": "MCQ",
            "difficulty": "EASY",
            "question_text": xss_payload,
            "options": {"A": "Option 1", "B": xss_payload, "C": "Option 3", "D": "Option 4"},
            "correct_answer": "A",
            "explanation": xss_payload,
            "status": "PUBLISHED",
        },
        headers=headers,
    )
    assert res.status_code == 200
    data = res.json()
    assert data["question_text"] == xss_payload

    # Retrieve question as student
    q_res = client.get(f"/api/v1/questions/{data['id']}")
    assert q_res.status_code == 200
    q_data = q_res.json()
    assert q_data["question_text"] == xss_payload
