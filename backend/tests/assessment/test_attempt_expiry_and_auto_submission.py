import uuid
from datetime import datetime, timedelta, timezone
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.app.models.attempt import Attempt
from backend.app.models.content import Question
from backend.app.models.quiz import Quiz, QuizQuestion
from backend.tests.helpers import create_test_taxonomy, get_student_auth_headers


def test_attempt_expiry_and_auto_finalization(client: TestClient, db_session: Session):
    student_headers = get_student_auth_headers(db_session)
    cat, exam, subj, topic = create_test_taxonomy(db_session)

    q1 = Question(
        id=f"q_exp_{uuid.uuid4().hex[:6]}",
        topic_id=topic.id,
        difficulty="MEDIUM",
        type="MCQ",
        question_text="Expiry question",
        correct_answer="A",
        explanation="Expl",
        status="PUBLISHED",
    )
    db_session.add(q1)
    db_session.flush()

    quiz = Quiz(subject_id=subj.id, title="Short Quiz", duration_minutes=1, status="PUBLISHED", is_published=True)
    db_session.add(quiz)
    db_session.flush()

    db_session.add(QuizQuestion(quiz_id=quiz.id, question_id=q1.id, sort_order=1, marks=1.0, negative_marks=0.0))
    db_session.flush()

    # Start attempt
    s_resp = client.post(f"/api/v1/quizzes/{quiz.id}/start", headers=student_headers)
    att_id = s_resp.json()["attempt"]["id"]

    # Submit answer
    client.post(f"/api/v1/attempts/{att_id}/responses", json={"question_id": q1.id, "selected_answer": "A"}, headers=student_headers)

    # Manually backdate attempt expiration timestamp to simulate time expiry
    attempt = db_session.get(Attempt, att_id)
    attempt.expires_at = datetime.now(timezone.utc) - timedelta(minutes=5)
    db_session.commit()

    # Attempting to submit another response after expiry should trigger auto-finalization and rejection
    q2_resp = client.post(f"/api/v1/attempts/{att_id}/responses", json={"question_id": q1.id, "selected_answer": "B"}, headers=student_headers)
    assert q2_resp.status_code == 403

    # Check result
    res_resp = client.get(f"/api/v1/attempts/{att_id}/result", headers=student_headers)
    assert res_resp.status_code == 200
    assert res_resp.json()["status"] in ["EXPIRED", "SUBMITTED"]
    assert res_resp.json()["score"] == 1.0
