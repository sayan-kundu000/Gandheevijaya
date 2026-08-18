import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.app.core.security import create_access_token, get_password_hash
from backend.app.models.user import User


def get_admin_auth_headers(db_session: Session) -> dict:
    admin_email = f"admin_{uuid.uuid4().hex[:8]}@example.com"
    admin = User(
        email=admin_email,
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


def test_exam_category_crud_flow(client: TestClient, db_session: Session):
    headers = get_admin_auth_headers(db_session)

    # 1. Create Category (Admin)
    cat_payload = {"name": "GATE Engineering", "slug": f"gate-{uuid.uuid4().hex[:6]}"}
    resp = client.post("/api/v1/exams/categories", json=cat_payload, headers=headers)
    assert resp.status_code == 201
    cat_id = resp.json()["id"]

    # 2. List Categories (Public)
    resp = client.get("/api/v1/exams/categories")
    assert resp.status_code == 200
    categories = resp.json()
    assert any(c["id"] == cat_id for c in categories)

    # 3. Create Exam under Category (Admin)
    exam_code = f"GATE_CS_{uuid.uuid4().hex[:6]}"
    exam_payload = {
        "category_id": cat_id,
        "name": "GATE Computer Science",
        "code": exam_code,
        "description": "GATE CS Examination",
    }
    resp = client.post("/api/v1/exams", json=exam_payload, headers=headers)
    assert resp.status_code == 201
    exam_id = resp.json()["id"]
    assert resp.json()["code"] == exam_code

    # 4. Get Exam by ID
    resp = client.get(f"/api/v1/exams/{exam_id}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "GATE Computer Science"

    # 5. List Exams filtered by Category
    resp = client.get(f"/api/v1/exams?category_id={cat_id}")
    assert resp.status_code == 200
    assert len(resp.json()) >= 1


def test_subject_crud_and_pagination(client: TestClient, db_session: Session):
    headers = get_admin_auth_headers(db_session)

    # Setup Exam
    cat_payload = {"name": "SSC Exams", "slug": f"ssc-{uuid.uuid4().hex[:6]}"}
    c_resp = client.post("/api/v1/exams/categories", json=cat_payload, headers=headers)
    cat_id = c_resp.json()["id"]

    exam_code = f"SSC_CGL_{uuid.uuid4().hex[:6]}"
    e_resp = client.post(
        "/api/v1/exams",
        json={"category_id": cat_id, "name": "SSC CGL Exam", "code": exam_code},
        headers=headers,
    )
    exam_id = e_resp.json()["id"]

    # Create Subject
    subj_code = f"QUANT_{uuid.uuid4().hex[:6]}"
    s_resp = client.post(
        "/api/v1/subjects",
        json={"exam_id": exam_id, "name": "Quantitative Aptitude", "code": subj_code},
        headers=headers,
    )
    assert s_resp.status_code == 201
    subj_id = s_resp.json()["id"]

    # List Subjects with Pagination
    resp = client.get(f"/api/v1/subjects?exam_id={exam_id}&page=1&page_size=10")
    assert resp.status_code == 200
    data = resp.json()
    assert "items" in data
    assert data["total"] >= 1
    assert data["page"] == 1
    assert any(s["id"] == subj_id for s in data["items"])
