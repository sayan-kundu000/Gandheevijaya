import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.tests.helpers import get_student_auth_headers


def test_performance_delta_api(client: TestClient, db_session: Session):
    student_headers = get_student_auth_headers(db_session)

    res = client.get("/api/v1/intelligence/student/performance-delta?days=7", headers=student_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["window_days"] == 7
    assert "accuracy_delta" in data
    assert "score_delta" in data
    assert "velocity_status" in data
