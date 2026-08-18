import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.app.models.content import Question
from backend.app.models.quiz import Quiz, QuizQuestion
from backend.app.services.scoring_service import ScoringService
from backend.tests.helpers import create_test_taxonomy, get_student_auth_headers


def test_scoring_and_negative_marking_service(db_session: Session):
    service = ScoringService()

    # MCQ Test
    q_mcq = Question(
        id="q_mcq_1",
        question_text="Sample MCQ",
        type="MCQ",
        difficulty="MEDIUM",
        correct_answer="opt_a",
        explanation="MCQ explanation",
    )
    res_correct = service.evaluate_question_response(q_mcq, "opt_a", 2.0, 0.66)
    assert res_correct.is_correct is True
    assert res_correct.marks_awarded == 2.0
    assert res_correct.penalty_deducted == 0.0

    res_wrong = service.evaluate_question_response(q_mcq, "opt_b", 2.0, 0.66)
    assert res_wrong.is_correct is False
    assert res_wrong.marks_awarded == -0.66
    assert res_wrong.penalty_deducted == 0.66

    res_unans = service.evaluate_question_response(q_mcq, None, 2.0, 0.66)
    assert res_unans.is_correct is False
    assert res_unans.marks_awarded == 0.0

    # NAT Test
    q_nat = Question(
        id="q_nat_1",
        question_text="Calculate value",
        type="NAT",
        difficulty="MEDIUM",
        correct_answer="15.5",
        explanation="NAT explanation",
    )
    res_nat_correct = service.evaluate_question_response(q_nat, "15.50", 1.0, 0.0)
    assert res_nat_correct.is_correct is True
    assert res_nat_correct.marks_awarded == 1.0

    res_nat_wrong = service.evaluate_question_response(q_nat, "10.0", 1.0, 0.0)
    assert res_nat_wrong.is_correct is False
    assert res_nat_wrong.marks_awarded == 0.0  # NAT has no negative penalty


def test_full_attempt_scoring_and_result_submission(client: TestClient, db_session: Session):
    student_headers = get_student_auth_headers(db_session)
    cat, exam, subj, topic = create_test_taxonomy(db_session)

    q1 = Question(
        id=f"q_sc_1_{uuid.uuid4().hex[:6]}",
        topic_id=topic.id,
        difficulty="MEDIUM",
        type="MCQ",
        question_text="Q1 text",
        correct_answer="A",
        explanation="Expl 1",
        status="PUBLISHED",
    )
    q2 = Question(
        id=f"q_sc_2_{uuid.uuid4().hex[:6]}",
        topic_id=topic.id,
        difficulty="MEDIUM",
        type="MCQ",
        question_text="Q2 text",
        correct_answer="B",
        explanation="Expl 2",
        status="PUBLISHED",
    )
    db_session.add_all([q1, q2])
    db_session.flush()

    quiz = Quiz(
        subject_id=subj.id,
        title="Array Test",
        duration_minutes=30,
        passing_score=1.0,
        status="PUBLISHED",
        is_published=True,
    )
    db_session.add(quiz)
    db_session.flush()

    db_session.add(QuizQuestion(quiz_id=quiz.id, question_id=q1.id, sort_order=1, marks=2.0, negative_marks=0.5))
    db_session.add(QuizQuestion(quiz_id=quiz.id, question_id=q2.id, sort_order=2, marks=2.0, negative_marks=0.5))
    db_session.flush()

    # Start attempt
    s_resp = client.post(f"/api/v1/quizzes/{quiz.id}/start", headers=student_headers)
    att_id = s_resp.json()["attempt"]["id"]

    # Submit Q1 correct, Q2 wrong
    client.post(f"/api/v1/attempts/{att_id}/responses", json={"question_id": q1.id, "selected_answer": "A"}, headers=student_headers)
    client.post(f"/api/v1/attempts/{att_id}/responses", json={"question_id": q2.id, "selected_answer": "Wrong"}, headers=student_headers)

    # Submit quiz
    sub_resp = client.post(f"/api/v1/attempts/{att_id}/submit", headers=student_headers)
    assert sub_resp.status_code == 200
    res = sub_resp.json()

    assert res["score"] == 1.5  # 2.0 - 0.5 = 1.5
    assert res["correct_count"] == 1
    assert res["incorrect_count"] == 1
    assert res["passed"] is True
