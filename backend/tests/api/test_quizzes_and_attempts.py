import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.app.core.security import create_access_token, get_password_hash
from backend.app.models.user import User


def create_user(db_session: Session, role: str) -> tuple[User, dict]:
    user = User(
        email=f"{role.lower()}_{uuid.uuid4().hex[:8]}@example.com",
        password_hash=get_password_hash("Pass1234!"),
        full_name=f"Test {role.capitalize()}",
        role=role,
        is_active=True,
    )
    db_session.add(user)
    db_session.flush()
    db_session.refresh(user)
    token = create_access_token(subject=user.id, role=role)
    headers = {"Authorization": f"Bearer {token}"}
    return user, headers


def test_full_quiz_attempt_and_evaluation_flow(client: TestClient, db_session: Session):
    admin_user, admin_headers = create_user(db_session, "ADMIN")
    student_user, student_headers = create_user(db_session, "STUDENT")

    # 1. Setup Subject & Question
    c_resp = client.post("/api/v1/exams/categories", json={"name": "GATE", "slug": f"g-{uuid.uuid4().hex[:6]}"}, headers=admin_headers)
    e_resp = client.post("/api/v1/exams", json={"category_id": c_resp.json()["id"], "name": "GATE CS", "code": f"G_{uuid.uuid4().hex[:6]}"}, headers=admin_headers)
    s_resp = client.post("/api/v1/subjects", json={"exam_id": e_resp.json()["id"], "name": "C Prog", "code": f"CP_{uuid.uuid4().hex[:6]}"}, headers=admin_headers)
    subject_id = s_resp.json()["id"]

    t_resp = client.post("/api/v1/topics", json={"subject_id": subject_id, "name": "Pointers"}, headers=admin_headers)
    topic_id = t_resp.json()["id"]

    q1_id = f"Q1-{uuid.uuid4().hex[:6]}"
    q2_id = f"Q2-{uuid.uuid4().hex[:6]}"

    client.post(
        "/api/v1/questions",
        json={
            "id": q1_id,
            "topic_id": topic_id,
            "difficulty": "easy",
            "type": "MCQ",
            "question_text": "What does dereferencing a pointer do?",
            "options": ["Accesses value", "Deletes variable", "Allocates memory"],
            "correct_answer": "Accesses value",
            "explanation": "Pointer dereferencing accesses the value stored at the target memory address.",
        },
        headers=admin_headers,
    )

    client.post(
        "/api/v1/questions",
        json={
            "id": q2_id,
            "topic_id": topic_id,
            "difficulty": "medium",
            "type": "MCQ",
            "question_text": "Size of int pointer on 64-bit architecture?",
            "options": ["8 bytes", "4 bytes", "2 bytes"],
            "correct_answer": "8 bytes",
            "explanation": "Pointers store 64-bit addresses (8 bytes) on 64-bit architectures.",
        },
        headers=admin_headers,
    )

    # 2. Admin creates Published Quiz
    quiz_payload = {
        "subject_id": subject_id,
        "title": "Pointers Diagnostic Quiz",
        "description": "Evaluate understanding of memory pointers",
        "duration_minutes": 30,
        "passing_score": 1.0,
        "is_published": True,
        "questions": [
            {"question_id": q1_id, "sort_order": 1, "marks": 2.0, "negative_marks": 0.5},
            {"question_id": q2_id, "sort_order": 2, "marks": 2.0, "negative_marks": 0.5},
        ],
    }
    q_resp = client.post("/api/v1/quizzes", json=quiz_payload, headers=admin_headers)
    assert q_resp.status_code == 201
    quiz_id = q_resp.json()["id"]
    assert q_resp.json()["total_marks"] == 4.0

    # 3. Student Starts Quiz Attempt
    start_resp = client.post(f"/api/v1/quizzes/{quiz_id}/start", headers=student_headers)
    assert start_resp.status_code == 201
    attempt_id = start_resp.json()["attempt"]["id"]
    questions = start_resp.json()["questions"]
    assert len(questions) == 2
    # Ensure correct answers are stripped during attempt!
    assert "correct_answer" not in questions[0]

    # 4. Student Submits Answers (Q1 correct, Q2 wrong)
    submit_payload = {
        "answers": [
            {"question_id": q1_id, "selected_answer": "Accesses value"},
            {"question_id": q2_id, "selected_answer": "4 bytes"},
        ]
    }
    submit_resp = client.post(f"/api/v1/attempts/{attempt_id}/submit", json=submit_payload, headers=student_headers)
    assert submit_resp.status_code == 200
    result = submit_resp.json()
    assert result["attempt_id"] == attempt_id
    assert result["score"] == 1.5  # 2.0 - 0.5 = 1.5
    assert result["passed"] is True
    assert result["correct_count"] == 1
    assert result["incorrect_count"] == 1

    # 5. Idempotency Check: Re-submitting returns finalized result idempotently or 409!
    re_submit = client.post(f"/api/v1/attempts/{attempt_id}/submit", json=submit_payload, headers=student_headers)
    assert re_submit.status_code in [200, 409]

    # 6. Post-Submission Review (/results/{attempt_id})
    res_resp = client.get(f"/api/v1/results/{attempt_id}", headers=student_headers)
    assert res_resp.status_code == 200
    res_data = res_resp.json()
    assert len(res_data["detailed_questions"]) == 2
    # Explanations ARE present post-submission!
    assert res_data["detailed_questions"][0]["explanation"] != ""

    # 7. IDOR Check: Other student attempting to view attempt result MUST receive 403 Forbidden!
    other_student, other_headers = create_user(db_session, "STUDENT")
    idor_resp = client.get(f"/api/v1/results/{attempt_id}", headers=other_headers)
    assert idor_resp.status_code == 403
