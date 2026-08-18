import uuid

import pytest
from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_role_escalation_in_register_ignored():
    uid = uuid.uuid4().hex[:8]
    email = f"attacker_{uid}@example.com"
    payload = {
        "email": email,
        "password": "Password123!",
        "full_name": "Attacker",
        "role": "ADMIN",  # Attacker attempts to claim ADMIN role in public registration!
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["role"] == "STUDENT"  # Server MUST enforce STUDENT role


def test_student_cannot_access_admin_endpoints():
    uid = uuid.uuid4().hex[:8]
    email = f"student_authz_{uid}@example.com"
    pwd = "Password123!"
    client.post("/api/v1/auth/register", json={"email": email, "password": pwd, "full_name": "Student Authz"})

    login_resp = client.post("/api/v1/auth/login", json={"email": email, "password": pwd})
    token = login_resp.json()["access_token"]

    # Student attempts to list all users (admin-only endpoint)
    response = client.get("/api/v1/users", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "FORBIDDEN"


def test_admin_can_access_admin_endpoints():
    from backend.app.core.database import SessionLocal
    from backend.app.core.security import create_access_token
    from backend.app.models.user import User

    db = SessionLocal()
    admin_user = db.query(User).filter(User.role == "ADMIN").first()
    db.close()

    assert admin_user is not None
    admin_token = create_access_token(subject=admin_user.id, role="ADMIN")

    response = client.get("/api/v1/users", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
