import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.tests.helpers import get_admin_auth_headers, get_student_auth_headers


def test_admin_dashboard_overview(client: TestClient, db_session: Session):
    admin_headers = get_admin_auth_headers(db_session)

    # 1. Admin dashboard overview API
    res = client.get("/api/v1/admin/dashboard", headers=admin_headers)
    assert res.status_code == 200
    data = res.json()
    assert "total_users" in data
    assert "total_students" in data
    assert "total_admins" in data
    assert "total_questions" in data
    assert "total_quizzes" in data
    assert "total_attempts" in data

    # 2. Backward compatible stats endpoint
    res_s = client.get("/api/v1/admin/stats", headers=admin_headers)
    assert res_s.status_code == 200
    assert res_s.json()["total_users"] == data["total_users"]
