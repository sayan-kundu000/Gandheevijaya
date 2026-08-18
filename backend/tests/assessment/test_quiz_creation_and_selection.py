import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.app.models.content import Question
from backend.app.services.question_selection_service import QuestionSelectionService
from backend.tests.helpers import create_test_taxonomy, get_admin_auth_headers, get_student_auth_headers


def test_quiz_creation_and_question_selection(client: TestClient, db_session: Session):
    admin_headers = get_admin_auth_headers(db_session)
    student_headers = get_student_auth_headers(db_session)

    # 1. Setup Taxonomy & Published Questions using helper
    cat, exam, subj, topic = create_test_taxonomy(db_session)

    # Add 5 published questions
    q_ids = []
    for i in range(5):
        q = Question(
            id=f"q_sel_{uuid.uuid4().hex[:6]}",
            topic_id=topic.id,
            question_text=f"Question {i+1}",
            type="MCQ",
            difficulty="MEDIUM",
            correct_answer="opt_a",
            explanation=f"Explanation for question {i+1}",
            options=["A", "B", "C", "D"],
            status="PUBLISHED",
        )
        db_session.add(q)
        q_ids.append(q.id)
    db_session.flush()

    # 2. Test Question Selection Service
    sel_service = QuestionSelectionService(db_session)
    selected = sel_service.validate_and_select_questions(
        requested_count=3,
        exam_id=exam.id,
        subject_id=subj.id,
        topic_id=topic.id,
        randomize=True,
    )
    assert len(selected) == 3

    # 3. Create Quiz via Admin API
    quiz_payload = {
        "exam_id": exam.id,
        "subject_id": subj.id,
        "topic_id": topic.id,
        "title": "C Pointers Challenge",
        "description": "Comprehensive Pointers Test",
        "quiz_type": "TOPIC_TEST",
        "duration_minutes": 15,
        "negative_marking": 0.25,
        "is_published": True,
    }
    resp = client.post("/api/v1/quizzes", json=quiz_payload, headers=admin_headers)
    assert resp.status_code == 201
    quiz_data = resp.json()
    assert quiz_data["status"] == "PUBLISHED"
    assert quiz_data["quiz_type"] == "TOPIC_TEST"

    # 4. Student List Quizzes Filter
    q_resp = client.get(f"/api/v1/quizzes?subject_id={subj.id}", headers=student_headers)
    assert q_resp.status_code == 200
    items = q_resp.json()["items"]
    assert any(q["id"] == quiz_data["id"] for q in items)
