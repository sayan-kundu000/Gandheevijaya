import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.user import User
from backend.tests.helpers import get_admin_auth_headers, get_student_auth_headers, get_student2_auth_headers


def test_admin_user_management_flow(client: TestClient, db_session: Session):
    admin_headers = get_admin_auth_headers(db_session)
    student_headers = get_student_auth_headers(db_session)
    student2_headers = get_student2_auth_headers(db_session)

    # Get the exact admin created for this test call
    admin_user = db_session.scalars(select(User).where(User.role == "ADMIN").order_by(User.created_at.desc())).first()
    student2_user = db_session.scalars(select(User).where(User.email.like("student2_%")).order_by(User.created_at.desc())).first()

    # 1. List users with search & role filter
    res = client.get("/api/v1/admin/users?role=STUDENT", headers=admin_headers)
    assert res.status_code == 200
    items = res.json()["items"]
    assert len(items) >= 2

    # 2. Get user detail (no credentials in payload)
    res_d = client.get(f"/api/v1/admin/users/{student2_user.id}", headers=admin_headers)
    assert res_d.status_code == 200
    d_data = res_d.json()
    assert "password_hash" not in d_data
    assert d_data["id"] == student2_user.id

    # 3. Disable student 2
    res_dis = client.post(f"/api/v1/admin/users/{student2_user.id}/disable", json={"reason": "Test disable"}, headers=admin_headers)
    assert res_dis.status_code == 200
    assert res_dis.json()["is_active"] is False

    # 4. Reactivate student 2
    res_re = client.post(f"/api/v1/admin/users/{student2_user.id}/reactivate", json={"reason": "Test reactivate"}, headers=admin_headers)
    assert res_re.status_code == 200
    assert res_re.json()["is_active"] is True

    # 5. Self-disable protection test (Admin cannot disable self)
    res_self = client.post(f"/api/v1/admin/users/{admin_user.id}/disable", headers=admin_headers)
    assert res_self.status_code == 403
    assert "Self-disable protection" in str(res_self.json())
