import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.app.models.content import Question
from backend.app.models.quiz import Quiz, QuizQuestion
from backend.tests.helpers import create_test_taxonomy, get_student_auth_headers


def test_student_intelligence_profile_and_quadrant_analysis(client: TestClient, db_session: Session):
    student_headers = get_student_auth_headers(db_session)
    cat, exam, subj, topic = create_test_taxonomy(db_session)

    uid = uuid.uuid4().hex[:6]
    q1 = Question(id=f"q_intel_1_{uid}", topic_id=topic.id, difficulty="MEDIUM", type="MCQ", question_text=f"Q1_intel_{uid}", correct_answer="A", explanation="E", status="PUBLISHED")
    db_session.add(q1)
    db_session.flush()

    quiz = Quiz(subject_id=subj.id, title="Intel Quiz", duration_minutes=10, status="PUBLISHED", is_published=True)
    db_session.add(quiz)
    db_session.flush()

    db_session.add(QuizQuestion(quiz_id=quiz.id, question_id=q1.id, sort_order=1, marks=1.0, negative_marks=0.0))
    db_session.flush()

    # Complete attempt
    s1 = client.post(f"/api/v1/quizzes/{quiz.id}/start", headers=student_headers)
    att_1 = s1.json()["attempt"]["id"]
    client.post(f"/api/v1/attempts/{att_1}/responses", json={"question_id": q1.id, "selected_answer": "A"}, headers=student_headers)
    client.post(f"/api/v1/attempts/{att_1}/submit", headers=student_headers)

    # 1. Student Intelligence Profile API
    res_prof = client.get("/api/v1/intelligence/student/profile", headers=student_headers)
    assert res_prof.status_code == 200
    p_data = res_prof.json()
    assert p_data["overall_accuracy"] == 100.0
    assert p_data["total_questions_attempted"] == 1
    assert "quadrant_status" in p_data

    # 2. Speed vs Accuracy Quadrant API
    res_quad = client.get("/api/v1/intelligence/student/speed-accuracy", headers=student_headers)
    assert res_quad.status_code == 200
    q_data = res_quad.json()
    assert "overall_quadrant" in q_data
    assert len(q_data["topics"]) >= 1
