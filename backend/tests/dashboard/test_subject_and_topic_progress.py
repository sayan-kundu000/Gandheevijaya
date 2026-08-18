import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.app.models.content import Question
from backend.app.models.quiz import Quiz, QuizQuestion
from backend.tests.helpers import create_test_taxonomy, get_student_auth_headers


def test_subject_and_topic_progress_aggregation(client: TestClient, db_session: Session):
    student_headers = get_student_auth_headers(db_session)
    cat, exam, subj, topic = create_test_taxonomy(db_session)

    uid = uuid.uuid4().hex[:6]
    q1 = Question(id=f"q_tp_1_{uid}", topic_id=topic.id, difficulty="MEDIUM", type="MCQ", question_text=f"Q1_tp_{uid}", correct_answer="A", explanation="E", status="PUBLISHED")
    q2 = Question(id=f"q_tp_2_{uid}", topic_id=topic.id, difficulty="MEDIUM", type="MCQ", question_text=f"Q2_tp_{uid}", correct_answer="B", explanation="E", status="PUBLISHED")
    db_session.add_all([q1, q2])
    db_session.flush()

    quiz = Quiz(subject_id=subj.id, topic_id=topic.id, title="Prog Quiz", duration_minutes=30, status="PUBLISHED", is_published=True)
    db_session.add(quiz)
    db_session.flush()

    db_session.add(QuizQuestion(quiz_id=quiz.id, question_id=q1.id, sort_order=1, marks=1.0, negative_marks=0.0))
    db_session.add(QuizQuestion(quiz_id=quiz.id, question_id=q2.id, sort_order=2, marks=1.0, negative_marks=0.0))
    db_session.flush()

    # Attempt 1
    s1 = client.post(f"/api/v1/quizzes/{quiz.id}/start", headers=student_headers)
    att_1 = s1.json()["attempt"]["id"]
    client.post(f"/api/v1/attempts/{att_1}/responses", json={"question_id": q1.id, "selected_answer": "A"}, headers=student_headers)
    client.post(f"/api/v1/attempts/{att_1}/responses", json={"question_id": q2.id, "selected_answer": "Wrong"}, headers=student_headers)
    client.post(f"/api/v1/attempts/{att_1}/submit", headers=student_headers)

    # 1. Subject Progress API
    res_s = client.get("/api/v1/dashboard/subjects", headers=student_headers)
    assert res_s.status_code == 200
    s_items = res_s.json()["items"]
    assert len(s_items) >= 1
    target_s = next(s for s in s_items if s["subject_id"] == subj.id)
    assert target_s["questions_attempted"] == 2
    assert target_s["correct_answers"] == 1
    assert target_s["accuracy"] == 50.0
    assert target_s["attempt_count"] == 1

    # 2. Topic Progress API
    res_t = client.get("/api/v1/dashboard/topics", headers=student_headers)
    assert res_t.status_code == 200
    t_items = res_t.json()["items"]
    target_t = next(t for t in t_items if t["topic_id"] == topic.id)
    assert target_t["questions_attempted"] == 2
    assert target_t["accuracy"] == 50.0
