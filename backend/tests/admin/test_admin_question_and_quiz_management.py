import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.tests.helpers import create_test_taxonomy, get_admin_auth_headers


def test_admin_question_and_quiz_management(client: TestClient, db_session: Session):
    admin_headers = get_admin_auth_headers(db_session)
    cat, exam, subj, topic = create_test_taxonomy(db_session)

    # 1. Create Question
    q_payload = {
        "topic_id": topic.id,
        "difficulty": "MEDIUM",
        "type": "MCQ",
        "question_text": "What is 2 + 2?",
        "options": {"A": "3", "B": "4", "C": "5", "D": "6"},
        "correct_answer": "B",
        "explanation": "2 + 2 = 4",
        "status": "DRAFT",
    }
    res_q = client.post("/api/v1/admin/questions", json=q_payload, headers=admin_headers)
    assert res_q.status_code == 200
    q_data = res_q.json()
    q_id = q_data["id"]
    assert q_data["status"] == "DRAFT"

    # 2. Update Question
    res_up = client.patch(f"/api/v1/admin/questions/{q_id}", json={"difficulty": "HARD", "status": "PUBLISHED"}, headers=admin_headers)
    assert res_up.status_code == 200
    assert res_up.json()["difficulty"] == "HARD"
    assert res_up.json()["status"] == "PUBLISHED"

    # 3. Publish Question explicitly
    res_pub = client.post(f"/api/v1/admin/questions/{q_id}/publish", headers=admin_headers)
    assert res_pub.status_code == 200
    assert res_pub.json()["status"] == "PUBLISHED"
