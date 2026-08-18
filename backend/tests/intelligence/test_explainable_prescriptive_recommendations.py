import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.tests.helpers import create_test_taxonomy, get_student_auth_headers


def test_prescriptive_recommendations_and_topic_matrix(client: TestClient, db_session: Session):
    student_headers = get_student_auth_headers(db_session)
    cat, exam, subj, topic = create_test_taxonomy(db_session)

    # 1. Prescriptive Recommendations API
    res_rec = client.get("/api/v1/intelligence/student/recommendations?limit=5", headers=student_headers)
    assert res_rec.status_code == 200
    rec_items = res_rec.json()["items"]
    assert len(rec_items) >= 1
    first_rec = rec_items[0]
    assert "priority_score" in first_rec
    assert "explanation_reason" in first_rec
    assert len(first_rec["explanation_reason"]) > 10

    # 2. Topic Performance Matrix API
    res_mat = client.get("/api/v1/intelligence/topics/matrix", headers=student_headers)
    assert res_mat.status_code == 200
    mat_items = res_mat.json()["items"]
    assert len(mat_items) >= 1
    assert "health_status" in mat_items[0]
