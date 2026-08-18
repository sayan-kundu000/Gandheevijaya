import pytest
from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_student_cannot_access_other_student_profile():
    # Register Student A
    client.post("/api/v1/auth/register", json={"email": "student_a_idor@example.com", "password": "Password123!", "full_name": "Student A"})
    login_a = client.post("/api/v1/auth/login", json={"email": "student_a_idor@example.com", "password": "Password123!"})
    student_a_id = login_a.json()["user"]["id"]

    # Register Student B
    client.post("/api/v1/auth/register", json={"email": "student_b_idor@example.com", "password": "Password123!", "full_name": "Student B"})
    login_b = client.post("/api/v1/auth/login", json={"email": "student_b_idor@example.com", "password": "Password123!"})
    token_b = login_b.json()["access_token"]

    # Student B attempts to fetch Student A's profile via GET /api/v1/users/{StudentA_ID}
    response = client.get(f"/api/v1/users/{student_a_id}", headers={"Authorization": f"Bearer {token_b}"})
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "FORBIDDEN"
    assert "You do not own this resource" in response.json()["error"]["message"]


def test_student_can_access_own_profile():
    # Register Student A
    client.post("/api/v1/auth/register", json={"email": "student_own_profile@example.com", "password": "Password123!", "full_name": "Student Own"})
    login_a = client.post("/api/v1/auth/login", json={"email": "student_own_profile@example.com", "password": "Password123!"})
    token_a = login_a.json()["access_token"]
    student_a_id = login_a.json()["user"]["id"]

    # Student A fetches own profile via GET /api/v1/users/{StudentA_ID}
    response = client.get(f"/api/v1/users/{student_a_id}", headers={"Authorization": f"Bearer {token_a}"})
    assert response.status_code == 200
    assert response.json()["id"] == student_a_id
