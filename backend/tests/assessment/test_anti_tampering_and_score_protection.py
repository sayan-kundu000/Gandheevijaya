import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.app.models.content import Question
from backend.app.models.quiz import Quiz, QuizQuestion
from backend.tests.helpers import create_test_taxonomy, get_student_auth_headers, get_student2_auth_headers


def test_anti_tampering_and_cross_user_isolation(client: TestClient, db_session: Session):
    student1_headers = get_student_auth_headers(db_session)
    student2_headers = get_student2_auth_headers(db_session)

    cat, exam, subj, topic = create_test_taxonomy(db_session)

    q1 = Question(
        id=f"q_sec_1_{uuid.uuid4().hex[:6]}",
        topic_id=topic.id,
        difficulty="MEDIUM",
        type="MCQ",
        question_text="Legitimate Q",
        correct_answer="A",
        explanation="Expl 1",
        status="PUBLISHED",
    )
    q2_foreign = Question(
        id=f"q_sec_foreign_{uuid.uuid4().hex[:6]}",
        topic_id=topic.id,
        difficulty="MEDIUM",
        type="MCQ",
        question_text="Foreign Q",
        correct_answer="B",
        explanation="Expl 2",
        status="PUBLISHED",
    )
    db_session.add_all([q1, q2_foreign])
    db_session.flush()

    quiz = Quiz(subject_id=subj.id, title="Security Quiz", duration_minutes=30, status="PUBLISHED", is_published=True)
    db_session.add(quiz)
    db_session.flush()

    db_session.add(QuizQuestion(quiz_id=quiz.id, question_id=q1.id, sort_order=1, marks=1.0, negative_marks=0.0))
    db_session.flush()

    # 1. Student 1 starts attempt
    s1_resp = client.post(f"/api/v1/quizzes/{quiz.id}/start", headers=student1_headers)
    att_id_1 = s1_resp.json()["attempt"]["id"]

    # 2. Student 2 attempts to access Student 1's attempt (IDOR protection)
    res_idor = client.get(f"/api/v1/attempts/{att_id_1}", headers=student2_headers)
    assert res_idor.status_code == 403

    # 3. Student 1 attempts to submit response for foreign question ID (Answer injection protection)
    res_inj = client.post(
        f"/api/v1/attempts/{att_id_1}/responses",
        json={"question_id": q2_foreign.id, "selected_answer": "B"},
        headers=student1_headers,
    )
    assert res_inj.status_code == 422

    # 4. Student 1 submits valid attempt
    client.post(
        f"/api/v1/attempts/{att_id_1}/responses",
        json={"question_id": q1.id, "selected_answer": "A"},
        headers=student1_headers,
    )
    client.post(f"/api/v1/attempts/{att_id_1}/submit", headers=student1_headers)

    # 5. Student 1 attempts to submit another response after finalization
    res_post_sub = client.post(
        f"/api/v1/attempts/{att_id_1}/responses",
        json={"question_id": q1.id, "selected_answer": "Wrong"},
        headers=student1_headers,
    )
    assert res_post_sub.status_code == 409
