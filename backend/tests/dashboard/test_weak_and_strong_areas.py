import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.app.models.content import Question
from backend.app.models.quiz import Quiz, QuizQuestion
from backend.tests.helpers import create_test_taxonomy, get_student_auth_headers


def test_weak_and_strong_area_classification(client: TestClient, db_session: Session):
    student_headers = get_student_auth_headers(db_session)
    cat, exam, subj, topic = create_test_taxonomy(db_session)

    # Create 3 questions for topic
    uid = uuid.uuid4().hex[:6]
    q1 = Question(id=f"q_ws_1_{uid}", topic_id=topic.id, difficulty="MEDIUM", type="MCQ", question_text=f"Q1_ws_{uid}", correct_answer="A", explanation="E", status="PUBLISHED")
    q2 = Question(id=f"q_ws_2_{uid}", topic_id=topic.id, difficulty="MEDIUM", type="MCQ", question_text=f"Q2_ws_{uid}", correct_answer="A", explanation="E", status="PUBLISHED")
    q3 = Question(id=f"q_ws_3_{uid}", topic_id=topic.id, difficulty="MEDIUM", type="MCQ", question_text=f"Q3_ws_{uid}", correct_answer="A", explanation="E", status="PUBLISHED")
    db_session.add_all([q1, q2, q3])
    db_session.flush()

    quiz = Quiz(subject_id=subj.id, topic_id=topic.id, title="WS Quiz", duration_minutes=30, status="PUBLISHED", is_published=True)
    db_session.add(quiz)
    db_session.flush()

    db_session.add(QuizQuestion(quiz_id=quiz.id, question_id=q1.id, sort_order=1, marks=1.0, negative_marks=0.0))
    db_session.add(QuizQuestion(quiz_id=quiz.id, question_id=q2.id, sort_order=2, marks=1.0, negative_marks=0.0))
    db_session.add(QuizQuestion(quiz_id=quiz.id, question_id=q3.id, sort_order=3, marks=1.0, negative_marks=0.0))
    db_session.flush()

    # Attempt 1: All correct (100% accuracy -> STRONG)
    s1 = client.post(f"/api/v1/quizzes/{quiz.id}/start", headers=student_headers)
    att_1 = s1.json()["attempt"]["id"]
    client.post(f"/api/v1/attempts/{att_1}/responses", json={"question_id": q1.id, "selected_answer": "A"}, headers=student_headers)
    client.post(f"/api/v1/attempts/{att_1}/responses", json={"question_id": q2.id, "selected_answer": "A"}, headers=student_headers)
    client.post(f"/api/v1/attempts/{att_1}/responses", json={"question_id": q3.id, "selected_answer": "A"}, headers=student_headers)
    client.post(f"/api/v1/attempts/{att_1}/submit", headers=student_headers)

    # 1. Strong areas check
    res_str = client.get("/api/v1/dashboard/strong-areas?min_attempts=3&threshold=80.0", headers=student_headers)
    assert res_str.status_code == 200
    strong_items = res_str.json()["items"]
    assert any(item["topic_id"] == topic.id for item in strong_items)

    # 2. Weak areas check (should be empty since accuracy is 100%)
    res_weak = client.get("/api/v1/dashboard/weak-areas?min_attempts=3&threshold=60.0", headers=student_headers)
    assert res_weak.status_code == 200
    weak_items = res_weak.json()["items"]
    assert not any(item["topic_id"] == topic.id for item in weak_items)
