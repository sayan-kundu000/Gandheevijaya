import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.app.models.content import Exam, ExamCategory, Question, Subject, Topic
from backend.app.models.quiz import Quiz, QuizQuestion
from backend.tests.helpers import create_test_taxonomy, get_student_auth_headers


def test_real_gate_content_assessment_flow(client: TestClient, db_session: Session):
    student_headers = get_student_auth_headers(db_session)
    cat, exam, subj, topic = create_test_taxonomy(db_session)

    # Create real GATE CS questions (C Programming & Data Structures)
    q_c = Question(
        id=f"GCS27-CP-E-MCQ-{uuid.uuid4().hex[:6]}",
        topic_id=topic.id,
        difficulty="medium",
        type="MCQ",
        question_text="What will be the output of printf('%d', sizeof(int*)); on 64-bit architecture?",
        options=["4", "8", "2", "16"],
        correct_answer="8",
        explanation="Pointer size on 64-bit architectures is 8 bytes.",
        status="PUBLISHED",
    )
    q_dsa = Question(
        id=f"GCS27-ALGO-H-NAT-{uuid.uuid4().hex[:6]}",
        topic_id=topic.id,
        difficulty="hard",
        type="NAT",
        question_text="What is the worst-case number of comparisons in QuickSort for n=10 elements?",
        options=None,
        correct_answer="45",
        explanation="Worst-case comparisons n*(n-1)/2 = 10*9/2 = 45.",
        status="PUBLISHED",
    )
    db_session.add_all([q_c, q_dsa])
    db_session.flush()

    quiz = Quiz(
        subject_id=subj.id,
        title="GATE CS Benchmark Quiz",
        quiz_type="MOCK_TEST",
        duration_minutes=60,
        passing_score=3.0,
        status="PUBLISHED",
        is_published=True,
    )
    db_session.add(quiz)
    db_session.flush()

    db_session.add(QuizQuestion(quiz_id=quiz.id, question_id=q_c.id, sort_order=1, marks=2.0, negative_marks=0.66))
    db_session.add(QuizQuestion(quiz_id=quiz.id, question_id=q_dsa.id, sort_order=2, marks=2.0, negative_marks=0.0))
    db_session.flush()

    # 1. Start attempt
    start_resp = client.post(f"/api/v1/quizzes/{quiz.id}/start", headers=student_headers)
    assert start_resp.status_code == 201
    att_id = start_resp.json()["attempt"]["id"]
    assigned_questions = start_resp.json()["questions"]
    assert len(assigned_questions) == 2

    # 2. Submit response for C question (correct: '8') and DSA question (correct NAT: '45')
    client.post(f"/api/v1/attempts/{att_id}/responses", json={"question_id": q_c.id, "selected_answer": "8"}, headers=student_headers)
    client.post(f"/api/v1/attempts/{att_id}/responses", json={"question_id": q_dsa.id, "selected_answer": "45.0"}, headers=student_headers)

    # 3. Finalize attempt
    sub_resp = client.post(f"/api/v1/attempts/{att_id}/submit", headers=student_headers)
    assert sub_resp.status_code == 200
    res = sub_resp.json()

    assert res["score"] == 4.0
    assert res["percentage"] == 100.0
    assert res["accuracy"] == 100.0
    assert res["passed"] is True
    assert res["correct_count"] == 2
