import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.tests.helpers import get_student_auth_headers


def test_intelligence_security_and_admin_endpoint_protection(client: TestClient, db_session: Session):
    student_headers = get_student_auth_headers(db_session)

    # 1. Student attempting admin item analysis endpoint MUST receive HTTP 403 Forbidden
    res_ia = client.get("/api/v1/intelligence/questions/item-analysis", headers=student_headers)
    assert res_ia.status_code == 403

    # 2. Student attempting admin content health anomalies endpoint MUST receive HTTP 403 Forbidden
    res_anom = client.get("/api/v1/intelligence/content-health/anomalies", headers=student_headers)
    assert res_anom.status_code == 403
