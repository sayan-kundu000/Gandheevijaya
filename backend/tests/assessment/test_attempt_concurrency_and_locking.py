import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.app.models.attempt import AttemptAnswer
from backend.app.models.content import Question
from backend.app.models.quiz import Quiz, QuizQuestion
from backend.tests.helpers import create_test_taxonomy, get_student_auth_headers, get_student2_auth_headers


def test_double_submission_idempotency_and_conflict(client: TestClient, db_session: Session):
    student_headers = get_student_auth_headers(db_session)
    cat, exam, subj, topic = create_test_taxonomy(db_session)

    q1 = Question(
        id=f"q_conc_1_{uuid.uuid4().hex[:6]}",
        topic_id=topic.id,
        difficulty="MEDIUM",
        type="MCQ",
        question_text="Concurrency Q1",
        correct_answer="opt_a",
        explanation="Expl",
        status="PUBLISHED",
    )
    db_session.add(q1)
    db_session.flush()

    quiz = Quiz(
        subject_id=subj.id,
        title="Concurrency Quiz",
        duration_minutes=30,
        passing_score=1.0,
        status="PUBLISHED",
        is_published=True,
    )
    db_session.add(quiz)
    db_session.flush()

    db_session.add(QuizQuestion(quiz_id=quiz.id, question_id=q1.id, sort_order=1, marks=2.0, negative_marks=0.5))
    db_session.flush()

    # 1. Start Attempt
    start_resp = client.post(f"/api/v1/quizzes/{quiz.id}/start", headers=student_headers)
    att_id = start_resp.json()["attempt"]["id"]

    # 2. Submit response
    client.post(f"/api/v1/attempts/{att_id}/responses", json={"question_id": q1.id, "selected_answer": "opt_a"}, headers=student_headers)

    # 3. Submit quiz attempt for finalization
    sub_1 = client.post(f"/api/v1/attempts/{att_id}/submit", headers=student_headers)
    assert sub_1.status_code == 200
    res1 = sub_1.json()
    assert res1["score"] == 2.0
    assert res1["status"] == "SUBMITTED"

    # 4. Duplicate submission attempt MUST return identical result idempotently (200 OK) without double scoring!
    sub_2 = client.post(f"/api/v1/attempts/{att_id}/submit", headers=student_headers)
    assert sub_2.status_code == 200
    res2 = sub_2.json()
    assert res2["score"] == 2.0
    assert res2["attempt_id"] == att_id


def test_unique_constraint_on_attempt_answers(db_session: Session):
    cat, exam, subj, topic = create_test_taxonomy(db_session)
    q1 = Question(
        id=f"q_uq_{uuid.uuid4().hex[:6]}",
        topic_id=topic.id,
        difficulty="MEDIUM",
        type="MCQ",
        question_text="UQ Question",
        correct_answer="A",
        explanation="Expl",
        status="PUBLISHED",
    )
    db_session.add(q1)
    db_session.flush()

    quiz = Quiz(subject_id=subj.id, title="UQ Quiz", duration_minutes=30, status="PUBLISHED", is_published=True)
    db_session.add(quiz)
    db_session.flush()

    # Create duplicate AttemptAnswer records directly to test DB UniqueConstraint
    att_id = str(uuid.uuid4())
    ans1 = AttemptAnswer(attempt_id=att_id, question_id=q1.id, selected_answer="A")
    ans2 = AttemptAnswer(attempt_id=att_id, question_id=q1.id, selected_answer="B")
    db_session.add(ans1)
    db_session.flush()

    db_session.add(ans2)
    with pytest.raises(Exception):
        db_session.flush()
    db_session.rollback()
