import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.app.models.content import Question
from backend.app.models.quiz import Quiz, QuizQuestion
from backend.tests.helpers import create_test_taxonomy, get_student_auth_headers


def test_option_randomization_stability_across_resumes(client: TestClient, db_session: Session):
    student_headers = get_student_auth_headers(db_session)
    cat, exam, subj, topic = create_test_taxonomy(db_session)

    q1 = Question(
        id=f"q_opt_rnd_{uuid.uuid4().hex[:6]}",
        topic_id=topic.id,
        difficulty="MEDIUM",
        type="MCQ",
        question_text="Sample MCQ with options",
        options=["Option A", "Option B", "Option C", "Option D"],
        correct_answer="Option A",
        explanation="Expl",
        status="PUBLISHED",
    )
    db_session.add(q1)
    db_session.flush()

    quiz = Quiz(
        subject_id=subj.id,
        title="Option Shuffling Quiz",
        duration_minutes=30,
        randomize_options=True,
        status="PUBLISHED",
        is_published=True,
    )
    db_session.add(quiz)
    db_session.flush()

    db_session.add(QuizQuestion(quiz_id=quiz.id, question_id=q1.id, sort_order=1, marks=1.0, negative_marks=0.0))
    db_session.flush()

    # 1. Start attempt
    start_resp = client.post(f"/api/v1/quizzes/{quiz.id}/start", headers=student_headers)
    assert start_resp.status_code == 201
    att_id = start_resp.json()["attempt"]["id"]
    initial_options = start_resp.json()["questions"][0]["options"]
    assert set(initial_options) == {"Option A", "Option B", "Option C", "Option D"}

    # 2. Resume attempt multiple times and verify option order remains 100% IDENTICAL
    for _ in range(3):
        res_resp = client.get(f"/api/v1/attempts/{att_id}", headers=student_headers)
        assert res_resp.status_code == 200
        resumed_options = res_resp.json()["questions"][0]["options"]
        assert resumed_options == initial_options
