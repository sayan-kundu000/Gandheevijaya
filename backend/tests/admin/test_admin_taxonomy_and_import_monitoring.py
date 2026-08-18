import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.content import ExamCategory
from backend.tests.helpers import get_admin_auth_headers


def test_admin_taxonomy_creation_and_import_monitoring(client: TestClient, db_session: Session):
    admin_headers = get_admin_auth_headers(db_session)

    category = db_session.scalars(select(ExamCategory)).first()
    if not category:
        category = ExamCategory(name="Test Cat", slug=f"cat_{uuid.uuid4().hex[:6]}")
        db_session.add(category)
        db_session.flush()

    # 1. Create Exam
    exam_code = f"EXAM_{uuid.uuid4().hex[:6].upper()}"
    res_e = client.post("/api/v1/admin/exams", json={"code": exam_code, "name": "Test Exam", "category_id": category.id}, headers=admin_headers)
    assert res_e.status_code == 200
    exam_id = res_e.json()["id"]

    # 2. Create Subject
    subj_code = f"SUBJ_{uuid.uuid4().hex[:6].upper()}"
    res_s = client.post("/api/v1/admin/subjects", json={"exam_id": exam_id, "code": subj_code, "name": "Test Subject"}, headers=admin_headers)
    assert res_s.status_code == 200
    subj_id = res_s.json()["id"]

    # 3. Create Topic
    top_code = f"TOP_{uuid.uuid4().hex[:6].upper()}"
    res_t = client.post("/api/v1/admin/topics", json={"subject_id": subj_id, "code": top_code, "name": "Test Topic"}, headers=admin_headers)
    assert res_t.status_code == 200
    assert res_t.json()["code"] == top_code

    # 4. List Import Jobs API
    res_imp = client.get("/api/v1/admin/imports", headers=admin_headers)
    assert res_imp.status_code == 200
    assert "items" in res_imp.json()
