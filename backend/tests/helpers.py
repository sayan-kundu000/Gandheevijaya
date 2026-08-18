import uuid
from sqlalchemy.orm import Session

from backend.app.core.security import create_access_token, get_password_hash
from backend.app.models.content import Exam, ExamCategory, Subject, Topic
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


def get_student_auth_headers(db_session: Session) -> dict:
    student_email = f"student_{uuid.uuid4().hex[:8]}@example.com"
    student = User(
        email=student_email,
        password_hash=get_password_hash("StudentPass123!"),
        full_name="Test Student",
        role="STUDENT",
        is_active=True,
    )
    db_session.add(student)
    db_session.flush()
    db_session.refresh(student)

    token = create_access_token(subject=student.id, role="STUDENT")
    return {"Authorization": f"Bearer {token}"}


def get_student2_auth_headers(db_session: Session) -> dict:
    student_email = f"student2_{uuid.uuid4().hex[:8]}@example.com"
    student = User(
        email=student_email,
        password_hash=get_password_hash("StudentPass123!"),
        full_name="Test Student 2",
        role="STUDENT",
        is_active=True,
    )
    db_session.add(student)
    db_session.flush()
    db_session.refresh(student)

    token = create_access_token(subject=student.id, role="STUDENT")
    return {"Authorization": f"Bearer {token}"}


def create_test_taxonomy(db_session: Session):
    cat = ExamCategory(name="Engineering", slug=f"eng-{uuid.uuid4().hex[:6]}")
    db_session.add(cat)
    db_session.flush()

    exam = Exam(category_id=cat.id, name="GATE CS", code=f"GATE_{uuid.uuid4().hex[:6]}", status="ACTIVE")
    db_session.add(exam)
    db_session.flush()

    subj = Subject(exam_id=exam.id, name="C Programming", code=f"C_{uuid.uuid4().hex[:6]}", status="ACTIVE")
    db_session.add(subj)
    db_session.flush()

    topic = Topic(subject_id=subj.id, name="Pointers", status="ACTIVE")
    db_session.add(topic)
    db_session.flush()

    return cat, exam, subj, topic
