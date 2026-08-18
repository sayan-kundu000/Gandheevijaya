import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.app.core.security import create_access_token, get_password_hash
from backend.app.models.user import User


def get_headers(db_session: Session, role: str = "ADMIN") -> dict:
    user = User(
        email=f"user_{uuid.uuid4().hex[:8]}@example.com",
        password_hash=get_password_hash("Pass1234!"),
        full_name=f"Test {role}",
        role=role,
        is_active=True,
    )
    db_session.add(user)
    db_session.flush()
    db_session.refresh(user)
    token = create_access_token(subject=user.id, role=role)
    return {"Authorization": f"Bearer {token}"}


def test_study_materials_crud_and_search(client: TestClient, db_session: Session):
    admin_headers = get_headers(db_session, "ADMIN")

    # Setup Exam & Subject
    c_resp = client.post("/api/v1/exams/categories", json={"name": "Bank", "slug": f"b-{uuid.uuid4().hex[:6]}"}, headers=admin_headers)
    e_resp = client.post("/api/v1/exams", json={"category_id": c_resp.json()["id"], "name": "PO", "code": f"P_{uuid.uuid4().hex[:6]}"}, headers=admin_headers)
    s_resp = client.post("/api/v1/subjects", json={"exam_id": e_resp.json()["id"], "name": "Reasoning", "code": f"R_{uuid.uuid4().hex[:6]}"}, headers=admin_headers)
    subject_id = s_resp.json()["id"]

    # Create Study Material
    mat_payload = {
        "subject_id": subject_id,
        "title": "Syllogism Mastering Guide",
        "content": "# Syllogism Rules\n1. All A are B.\n2. Some B are C.",
        "media_urls": ["https://cdn.gandheevijaya.com/docs/syllogism.pdf"],
    }
    m_resp = client.post("/api/v1/materials", json=mat_payload, headers=admin_headers)
    assert m_resp.status_code == 201
    mat_id = m_resp.json()["id"]

    # List Study Materials with Search Filter
    s_resp = client.get(f"/api/v1/materials?subject_id={subject_id}&search=Syllogism")
    assert s_resp.status_code == 200
    items = s_resp.json()["items"]
    assert len(items) >= 1
    assert items[0]["id"] == mat_id


def test_analytics_and_admin_stats(client: TestClient, db_session: Session):
    admin_headers = get_headers(db_session, "ADMIN")
    student_headers = get_headers(db_session, "STUDENT")

    # 1. Get Student Analytics (/analytics/me)
    me_resp = client.get("/api/v1/analytics/me", headers=student_headers)
    assert me_resp.status_code == 200
    data = me_resp.json()
    assert "overall_accuracy" in data
    assert "subject_performance" in data

    # 2. Get Leaderboard
    lb_resp = client.get("/api/v1/leaderboard")
    assert lb_resp.status_code == 200
    assert isinstance(lb_resp.json(), list)

    # 3. Get Admin Dashboard Stats
    stats_resp = client.get("/api/v1/admin/stats", headers=admin_headers)
    assert stats_resp.status_code == 200
    stats = stats_resp.json()
    assert stats["total_users"] >= 2
    assert stats["total_students"] >= 1
    assert stats["total_admins"] >= 1

    # 4. Non-admin accessing admin stats MUST receive 403 Forbidden
    forbidden_resp = client.get("/api/v1/admin/stats", headers=student_headers)
    assert forbidden_resp.status_code == 403
