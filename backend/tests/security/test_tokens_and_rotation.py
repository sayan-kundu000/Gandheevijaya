import uuid
from datetime import timedelta

import pytest
from fastapi.testclient import TestClient

from backend.app.core.security import create_access_token
from backend.app.main import app

client = TestClient(app)


def test_expired_access_token_rejected():
    expired_token = create_access_token(
        subject="user_uuid_expired",
        role="STUDENT",
        expires_delta=timedelta(seconds=-10),
    )
    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {expired_token}"})
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "UNAUTHORIZED"


def test_refresh_token_rotation():
    uid = uuid.uuid4().hex[:8]
    email = f"rotation_user_{uid}@example.com"
    pwd = "Password123!"
    reg_resp = client.post("/api/v1/auth/register", json={"email": email, "password": pwd, "full_name": "Rotation User"})
    assert reg_resp.status_code == 201

    login_resp = client.post("/api/v1/auth/login", json={"email": email, "password": pwd})
    assert login_resp.status_code == 200
    refresh_cookie = login_resp.cookies.get("refresh_token")
    assert refresh_cookie is not None

    # Perform refresh rotation
    client.cookies.set("refresh_token", refresh_cookie)
    refresh_resp = client.post("/api/v1/auth/refresh")
    assert refresh_resp.status_code == 200
    new_access_token = refresh_resp.json()["access_token"]
    new_refresh_cookie = refresh_resp.cookies.get("refresh_token")

    assert new_access_token is not None
    assert new_refresh_cookie is not None
    assert new_refresh_cookie != refresh_cookie


def test_token_reuse_attack_revokes_family():
    uid = uuid.uuid4().hex[:8]
    email = f"reuse_user_{uid}@example.com"
    pwd = "Password123!"
    reg_resp = client.post("/api/v1/auth/register", json={"email": email, "password": pwd, "full_name": "Reuse User"})
    assert reg_resp.status_code == 201

    login_resp = client.post("/api/v1/auth/login", json={"email": email, "password": pwd})
    assert login_resp.status_code == 200
    initial_refresh_cookie = login_resp.cookies.get("refresh_token")

    # Legitimate refresh 1
    client.cookies.set("refresh_token", initial_refresh_cookie)
    refresh_resp1 = client.post("/api/v1/auth/refresh")
    assert refresh_resp1.status_code == 200
    legitimate_refresh_cookie2 = refresh_resp1.cookies.get("refresh_token")

    # Replay attack: Attacker tries to reuse initial_refresh_cookie after it was already rotated
    client.cookies.set("refresh_token", initial_refresh_cookie)
    attack_resp = client.post("/api/v1/auth/refresh")
    assert attack_resp.status_code == 401
    assert "Security alert" in attack_resp.json()["error"]["message"]

    # Now the legitimate client tries to use legitimate_refresh_cookie2 -> Must also be blocked because entire family was invalidated!
    client.cookies.set("refresh_token", legitimate_refresh_cookie2)
    blocked_resp = client.post("/api/v1/auth/refresh")
    assert blocked_resp.status_code == 401


def test_logout():
    uid = uuid.uuid4().hex[:8]
    email = f"logout_user_{uid}@example.com"
    pwd = "Password123!"
    reg_resp = client.post("/api/v1/auth/register", json={"email": email, "password": pwd, "full_name": "Logout User"})
    assert reg_resp.status_code == 201

    login_resp = client.post("/api/v1/auth/login", json={"email": email, "password": pwd})
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]

    logout_resp = client.post("/api/v1/auth/logout", headers={"Authorization": f"Bearer {token}"})
    assert logout_resp.status_code == 200

    # Refresh attempt after logout should fail
    refresh_resp = client.post("/api/v1/auth/refresh")
    assert refresh_resp.status_code == 401
