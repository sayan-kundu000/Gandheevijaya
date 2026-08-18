import uuid

import pytest
from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_register_student_success():
    uid = uuid.uuid4().hex[:8]
    email = f"student_reg_{uid}@example.com"
    payload = {
        "email": email,
        "password": "Password123!",
        "full_name": "Test Student",
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == email
    assert data["role"] == "STUDENT"
    assert data["is_active"] is True
    assert "password_hash" not in data


def test_register_duplicate_email_rejected():
    uid = uuid.uuid4().hex[:8]
    email = f"student_dup_{uid}@example.com"
    payload = {
        "email": email,
        "password": "Password123!",
        "full_name": "Test Student Dup",
    }
    response1 = client.post("/api/v1/auth/register", json=payload)
    assert response1.status_code == 201

    response2 = client.post("/api/v1/auth/register", json=payload)
    assert response2.status_code == 409
    data = response2.json()
    assert data["error"]["code"] == "RESOURCE_CONFLICT"


def test_login_success():
    uid = uuid.uuid4().hex[:8]
    email = f"login_success_{uid}@example.com"
    reg_payload = {
        "email": email,
        "password": "Password123!",
        "full_name": "Login Success User",
    }
    client.post("/api/v1/auth/register", json=reg_payload)

    login_payload = {
        "email": email,
        "password": "Password123!",
    }
    response = client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == email


def test_login_invalid_password_returns_generic_error():
    uid = uuid.uuid4().hex[:8]
    email = f"login_fail_{uid}@example.com"
    client.post("/api/v1/auth/register", json={"email": email, "password": "Password123!", "full_name": "User"})

    login_payload = {
        "email": email,
        "password": "WrongPassword123!",
    }
    response = client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 401
    data = response.json()
    assert data["error"]["message"] == "Invalid email or password."


def test_login_nonexistent_email_returns_generic_error():
    login_payload = {
        "email": f"nonexistent_{uuid.uuid4().hex[:8]}@example.com",
        "password": "Password123!",
    }
    response = client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 401
    data = response.json()
    assert data["error"]["message"] == "Invalid email or password."


def test_get_me_authenticated():
    uid = uuid.uuid4().hex[:8]
    email = f"get_me_{uid}@example.com"
    reg_payload = {
        "email": email,
        "password": "Password123!",
        "full_name": "Get Me User",
    }
    client.post("/api/v1/auth/register", json=reg_payload)

    login_resp = client.post("/api/v1/auth/login", json={"email": email, "password": "Password123!"})
    token = login_resp.json()["access_token"]

    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == email
