import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.app.models.content import Question
from backend.tests.helpers import create_test_taxonomy, get_admin_auth_headers


def test_item_analysis_and_option_distractor_diagnostics(client: TestClient, db_session: Session):
    admin_headers = get_admin_auth_headers(db_session)
    cat, exam, subj, topic = create_test_taxonomy(db_session)

    q = Question(
        id=f"q_item_ana_{uuid.uuid4().hex[:6]}",
        topic_id=topic.id,
        difficulty="HARD",
        type="MCQ",
        question_text="Sample MCQ Question",
        options={"A": "Option 1", "B": "Option 2", "C": "Option 3", "D": "Option 4"},
        correct_answer="B",
        explanation="Explanation",
        status="PUBLISHED",
    )
    db_session.add(q)
    db_session.flush()

    # 1. Question Item Analysis API
    res_ia = client.get(f"/api/v1/intelligence/questions/item-analysis?topic_id={topic.id}", headers=admin_headers)
    assert res_ia.status_code == 200
    items = res_ia.json()["items"]
    assert any(i["question_id"] == q.id for i in items)

    # 2. Option Distractor Analysis API
    res_opt = client.get(f"/api/v1/intelligence/questions/{q.id}/option-analysis", headers=admin_headers)
    assert res_opt.status_code == 200
    opt_data = res_opt.json()
    assert opt_data["question_id"] == q.id
    assert len(opt_data["options"]) == 4

    # 3. Content Health Anomalies API
    res_anom = client.get("/api/v1/intelligence/content-health/anomalies", headers=admin_headers)
    assert res_anom.status_code == 200
    assert "items" in res_anom.json()
