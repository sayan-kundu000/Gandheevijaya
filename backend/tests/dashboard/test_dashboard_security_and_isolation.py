import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.app.models.content import Question
from backend.app.models.quiz import Quiz, QuizQuestion
from backend.tests.helpers import create_test_taxonomy, get_student_auth_headers, get_student2_auth_headers


def test_cross_user_dashboard_data_isolation(client: TestClient, db_session: Session):
    student1_headers = get_student_auth_headers(db_session)
    student2_headers = get_student2_auth_headers(db_session)

    cat, exam, subj, topic = create_test_taxonomy(db_session)

    q1 = Question(id=f"q_iso_1_{uuid.uuid4().hex[:6]}", topic_id=topic.id, difficulty="MEDIUM", type="MCQ", question_text="Q1", correct_answer="A", explanation="E", status="PUBLISHED")
    db_session.add(q1)
    db_session.flush()

    quiz = Quiz(subject_id=subj.id, title="Isolation Quiz", duration_minutes=10, status="PUBLISHED", is_published=True)
    db_session.add(quiz)
    db_session.flush()

    db_session.add(QuizQuestion(quiz_id=quiz.id, question_id=q1.id, sort_order=1, marks=1.0, negative_marks=0.0))
    db_session.flush()

    # Student 1 completes attempt
    s1 = client.post(f"/api/v1/quizzes/{quiz.id}/start", headers=student1_headers)
    att_1 = s1.json()["attempt"]["id"]
    client.post(f"/api/v1/attempts/{att_1}/responses", json={"question_id": q1.id, "selected_answer": "A"}, headers=student1_headers)
    client.post(f"/api/v1/attempts/{att_1}/submit", headers=student1_headers)

    # 1. Student 1 dashboard shows 1 attempt
    s1_dash = client.get("/api/v1/dashboard/overview", headers=student1_headers).json()
    assert s1_dash["completed_attempts"] == 1
    assert s1_dash["questions_attempted"] == 1

    # 2. Student 2 dashboard MUST show ZERO attempts (100% data isolation guaranteed!)
    s2_dash = client.get("/api/v1/dashboard/overview", headers=student2_headers).json()
    assert s2_dash["completed_attempts"] == 0
    assert s2_dash["questions_attempted"] == 0
    assert s2_dash["active_attempts"] == 0
