import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.tests.helpers import get_admin_auth_headers, get_student_auth_headers


def test_admin_authorization_and_audit_logging(client: TestClient, db_session: Session):
    student_headers = get_student_auth_headers(db_session)
    admin_headers = get_admin_auth_headers(db_session)

    # 1. Student attempting admin dashboard endpoint MUST receive HTTP 403 Forbidden
    res_st = client.get("/api/v1/admin/dashboard", headers=student_headers)
    assert res_st.status_code == 403

    res_st_u = client.get("/api/v1/admin/users", headers=student_headers)
    assert res_st_u.status_code == 403

    # 2. Admin audit log endpoint
    res_audit = client.get("/api/v1/admin/audit-logs", headers=admin_headers)
    assert res_audit.status_code == 200
    assert "items" in res_audit.json()
