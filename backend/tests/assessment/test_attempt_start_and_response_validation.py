import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.app.models.content import Question
from backend.app.models.quiz import Quiz, QuizQuestion
from backend.tests.helpers import create_test_taxonomy, get_student_auth_headers


def test_attempt_start_and_single_response_flow(client: TestClient, db_session: Session):
    student_headers = get_student_auth_headers(db_session)

    # Setup Taxonomy
    cat, exam, subj, topic = create_test_taxonomy(db_session)

    q1 = Question(
        id=f"q_att_{uuid.uuid4().hex[:6]}",
        topic_id=topic.id,
        question_text="What is the height of a balanced BST?",
        type="MCQ",
        difficulty="MEDIUM",
        correct_answer="opt_b",
        options=["O(n)", "O(log n)", "O(1)", "O(n log n)"],
        explanation="Balanced BST height is O(log n).",
        status="PUBLISHED",
    )
    db_session.add(q1)
    db_session.flush()

    quiz = Quiz(
        subject_id=subj.id,
        topic_id=topic.id,
        title="Tree Structures Test",
        duration_minutes=20,
        status="PUBLISHED",
        is_published=True,
    )
    db_session.add(quiz)
    db_session.flush()

    assoc = QuizQuestion(quiz_id=quiz.id, question_id=q1.id, sort_order=1, marks=2.0, negative_marks=0.66)
    db_session.add(assoc)
    db_session.flush()

    # 1. Start Quiz Attempt
    start_resp = client.post(f"/api/v1/quizzes/{quiz.id}/start", headers=student_headers)
    assert start_resp.status_code == 201
    att_data = start_resp.json()["attempt"]
    attempt_id = att_data["id"]
    questions = start_resp.json()["questions"]
    assert len(questions) == 1

    # Verify answers/explanations stripped from student question payload
    assert "correct_answer" not in questions[0]
    assert "explanation" not in questions[0]

    # 2. Single Response Submission
    resp_payload = {"question_id": q1.id, "selected_answer": "opt_b"}
    s_resp = client.post(f"/api/v1/attempts/{attempt_id}/responses", json=resp_payload, headers=student_headers)
    assert s_resp.status_code == 200
    assert s_resp.json()["selected_answer"] == "opt_b"

    # 3. Resume Attempt
    res_resp = client.get(f"/api/v1/attempts/{attempt_id}", headers=student_headers)
    assert res_resp.status_code == 200
    assert res_resp.json()["answers_map"][q1.id] == "opt_b"
