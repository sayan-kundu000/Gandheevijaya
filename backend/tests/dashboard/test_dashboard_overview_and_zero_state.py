import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.tests.helpers import create_test_taxonomy, get_student_auth_headers


def test_new_student_zero_state_dashboard(client: TestClient, db_session: Session):
    student_headers = get_student_auth_headers(db_session)

    # 1. Overview zero state
    res = client.get("/api/v1/dashboard/overview", headers=student_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["total_attempts"] == 0
    assert data["completed_attempts"] == 0
    assert data["active_attempts"] == 0
    assert data["overall_accuracy"] == 0.0
    assert data["average_percentage"] == 0.0

    # 2. Compact dashboard zero state
    res_c = client.get("/api/v1/dashboard", headers=student_headers)
    assert res_c.status_code == 200
    data_c = res_c.json()
    assert data_c["overview"]["total_attempts"] == 0
    assert data_c["recent_activity"] == []
    assert data_c["weak_areas"] == []
    assert data_c["strong_areas"] == []
    assert data_c["consistency"]["active_study_days"] == 0
