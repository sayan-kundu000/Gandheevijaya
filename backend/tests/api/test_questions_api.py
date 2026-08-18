import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.app.core.security import create_access_token, get_password_hash
from backend.app.models.user import User


def get_admin_headers(db_session: Session) -> dict:
    admin = User(
        email=f"admin_{uuid.uuid4().hex[:8]}@example.com",
        password_hash=get_password_hash("AdminPass123!"),
        full_name="Test Admin",
        role="ADMIN",
        is_active=True,
    )
    db_session.add(admin)
    db_session.flush()
    db_session.refresh(admin)
    token = create_access_token(subject=admin.id, role="ADMIN")
    return {"Authorization": f"Bearer {token}"}


def get_student_headers(db_session: Session) -> dict:
    student = User(
        email=f"student_{uuid.uuid4().hex[:8]}@example.com",
        password_hash=get_password_hash("StudentPass123!"),
        full_name="Test Student",
        role="STUDENT",
        is_active=True,
    )
    db_session.add(student)
    db_session.flush()
    db_session.refresh(student)
    token = create_access_token(subject=student.id, role="STUDENT")
    return {"Authorization": f"Bearer {token}"}


def setup_topic(client: TestClient, admin_headers: dict) -> int:
    # Exam & Subject
    c_resp = client.post("/api/v1/exams/categories", json={"name": "Tech", "slug": f"t-{uuid.uuid4().hex[:6]}"}, headers=admin_headers)
    e_resp = client.post("/api/v1/exams", json={"category_id": c_resp.json()["id"], "name": "CS", "code": f"C_{uuid.uuid4().hex[:6]}"}, headers=admin_headers)
    s_resp = client.post("/api/v1/subjects", json={"exam_id": e_resp.json()["id"], "name": "DS", "code": f"D_{uuid.uuid4().hex[:6]}"}, headers=admin_headers)
    t_resp = client.post("/api/v1/topics", json={"subject_id": s_resp.json()["id"], "name": "Arrays"}, headers=admin_headers)
    return t_resp.json()["id"]


def test_question_answer_leakage_protection(client: TestClient, db_session: Session):
    admin_headers = get_admin_headers(db_session)
    student_headers = get_student_headers(db_session)
    topic_id = setup_topic(client, admin_headers)

    q_id = f"QTEST-{uuid.uuid4().hex[:8]}"
    q_payload = {
        "id": q_id,
        "topic_id": topic_id,
        "difficulty": "easy",
        "type": "MCQ",
        "question_text": "What is the time complexity of array lookup by index?",
        "options": ["O(1)", "O(n)", "O(log n)", "O(n^2)"],
        "correct_answer": "O(1)",
        "explanation": "Array indexing is direct memory offset access in constant time O(1).",
        "tags": ["basics", "data structures"],
    }

    # 1. Admin creates question
    resp = client.post("/api/v1/questions", json=q_payload, headers=admin_headers)
    assert resp.status_code == 201
    assert resp.json()["correct_answer"] == "O(1)"
    assert resp.json()["explanation"] == "Array indexing is direct memory offset access in constant time O(1)."

    # 2. Student queries questions list -> MUST STRIP correct_answer & explanation!
    resp = client.get(f"/api/v1/questions?topic_id={topic_id}", headers=student_headers)
    assert resp.status_code == 200
    item = resp.json()["items"][0]
    assert "correct_answer" not in item
    assert "explanation" not in item
    assert item["question_text"] == "What is the time complexity of array lookup by index?"

    # 3. Student fetches single question -> MUST STRIP correct_answer & explanation!
    resp = client.get(f"/api/v1/questions/{q_id}", headers=student_headers)
    assert resp.status_code == 200
    q_data = resp.json()
    assert "correct_answer" not in q_data
    assert "explanation" not in q_data

    # 4. Admin fetches single question -> MUST INCLUDE correct_answer & explanation!
    resp = client.get(f"/api/v1/questions/{q_id}", headers=admin_headers)
    assert resp.status_code == 200
    admin_data = resp.json()
    assert admin_data["correct_answer"] == "O(1)"
    assert admin_data["explanation"] == "Array indexing is direct memory offset access in constant time O(1)."
