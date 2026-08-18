import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.app.models.content import Question
from backend.app.models.quiz import Quiz, QuizQuestion
from backend.tests.helpers import create_test_taxonomy, get_student_auth_headers


def test_performance_trends_and_study_consistency(client: TestClient, db_session: Session):
    student_headers = get_student_auth_headers(db_session)
    cat, exam, subj, topic = create_test_taxonomy(db_session)

    uid = uuid.uuid4().hex[:6]
    q1 = Question(id=f"q_tc_1_{uid}", topic_id=topic.id, difficulty="MEDIUM", type="MCQ", question_text=f"Q1_tc_{uid}", correct_answer="A", explanation="E", status="PUBLISHED")
    db_session.add(q1)
    db_session.flush()

    quiz = Quiz(subject_id=subj.id, title="Trend Quiz", duration_minutes=10, status="PUBLISHED", is_published=True)
    db_session.add(quiz)
    db_session.flush()

    db_session.add(QuizQuestion(quiz_id=quiz.id, question_id=q1.id, sort_order=1, marks=1.0, negative_marks=0.0))
    db_session.flush()

    # Complete attempt
    s1 = client.post(f"/api/v1/quizzes/{quiz.id}/start", headers=student_headers)
    att_1 = s1.json()["attempt"]["id"]
    client.post(f"/api/v1/attempts/{att_1}/responses", json={"question_id": q1.id, "selected_answer": "A"}, headers=student_headers)
    client.post(f"/api/v1/attempts/{att_1}/submit", headers=student_headers)

    # 1. Performance Trends API
    res_tr = client.get("/api/v1/dashboard/performance-trends?days=30", headers=student_headers)
    assert res_tr.status_code == 200
    tr_items = res_tr.json()["items"]
    assert len(tr_items) >= 1
    assert tr_items[0]["attempts_count"] >= 1
    assert tr_items[0]["accuracy"] == 100.0

    # 2. Consistency API
    res_con = client.get("/api/v1/dashboard/consistency", headers=student_headers)
    assert res_con.status_code == 200
    con_data = res_con.json()
    assert con_data["active_study_days"] >= 1
    assert con_data["current_streak_days"] >= 1
    assert con_data["longest_streak_days"] >= 1
