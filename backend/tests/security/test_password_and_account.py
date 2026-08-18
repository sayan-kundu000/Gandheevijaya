import uuid

import pytest
from fastapi.testclient import TestClient

from backend.app.core.database import SessionLocal
from backend.app.core.security import create_access_token, get_password_hash, verify_password
from backend.app.main import app
from backend.app.models.user import User

client = TestClient(app)


def test_argon2id_password_hashing():
    raw_pwd = "MySuperSecretPassword123!"
    hashed = get_password_hash(raw_pwd)

    assert hashed != raw_pwd
    assert hashed.startswith("$argon2id$")
    assert verify_password(raw_pwd, hashed) is True
    assert verify_password("WrongPassword!", hashed) is False


def test_password_change_invalidates_active_sessions():
    uid = uuid.uuid4().hex[:8]
    email = f"pwd_change_{uid}@example.com"
    pwd = "OldPassword123!"
    reg_resp = client.post("/api/v1/auth/register", json={"email": email, "password": pwd, "full_name": "Pwd Change User"})
    assert reg_resp.status_code == 201

    login_resp = client.post("/api/v1/auth/login", json={"email": email, "password": pwd})
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]

    # Perform password change
    change_resp = client.post(
        "/api/v1/auth/change-password",
        headers={"Authorization": f"Bearer {token}"},
        json={"current_password": pwd, "new_password": "NewPassword123!"},
    )
    assert change_resp.status_code == 200

    # Old login credentials must fail
    login_old = client.post("/api/v1/auth/login", json={"email": email, "password": pwd})
    assert login_old.status_code == 401

    # New login credentials must succeed
    login_new = client.post("/api/v1/auth/login", json={"email": email, "password": "NewPassword123!"})
    assert login_new.status_code == 200


def test_disabled_account_blocked():
    uid = uuid.uuid4().hex[:8]
    email = f"disabled_user_{uid}@example.com"
    pwd = "Password123!"
    reg_resp = client.post("/api/v1/auth/register", json={"email": email, "password": pwd, "full_name": "Disabled User"})
    assert reg_resp.status_code == 201

    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    user_id = user.id
    user.is_active = False
    db.commit()
    db.close()

    # Login must fail for disabled user
    login_resp = client.post("/api/v1/auth/login", json={"email": email, "password": pwd})
    assert login_resp.status_code == 401
    assert "disabled" in login_resp.json()["error"]["message"].lower()

    # Access API with pre-issued token for disabled user must fail
    token = create_access_token(subject=user_id, role="STUDENT")
    me_resp = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_resp.status_code == 401
    assert "disabled" in me_resp.json()["error"]["message"].lower()
