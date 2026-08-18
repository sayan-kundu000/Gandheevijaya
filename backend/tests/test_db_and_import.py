import os
import sys

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Adjust python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.app.core.database import Base
from backend.app.models.content import Exam, ExamCategory, Subject
from backend.app.models.material import StudyMaterial
from scripts.import_questions import validate_question_data

# Use in-memory SQLite for testing DB operations
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def db_session():
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionTesting()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_models_creation(db_session):
    # Test ExamCategory & Exam
    cat = ExamCategory(name="GATE Test", slug="gate-test")
    db_session.add(cat)
    db_session.commit()
    assert cat.id is not None

    exam = Exam(category_id=cat.id, name="GATE CS Test", code="GATE_CS_TEST")
    db_session.add(exam)
    db_session.commit()
    assert exam.id is not None

    # Test Subject
    subj = Subject(exam_id=exam.id, name="C Programming Test", code="CPROG_TEST")
    db_session.add(subj)
    db_session.commit()
    assert subj.id is not None

    # Test StudyMaterial
    material = StudyMaterial(
        subject_id=subj.id,
        title="Pointer Basics",
        content="# Pointer Basics\nContent Details",
        media_urls=["http://test.com/link"]
    )
    db_session.add(material)
    db_session.commit()
    assert material.id is not None
    assert material.title == "Pointer Basics"
    assert material.content == "# Pointer Basics\nContent Details"

def test_validation_function():
    # Valid Question MCQ
    q = {
        "id": "GCS27-PDS-E-MCQ-100",
        "subject": "PDS",
        "topic": "Pointers",
        "difficulty": "easy",
        "type": "MCQ",
        "question": "What is 1+1?",
        "options": ["1", "2", "3", "4"]
    }
    ans = {"id": "GCS27-PDS-E-MCQ-100", "correct_answer": "B"}
    soln = {"id": "GCS27-PDS-E-MCQ-100", "explanation": "Simple arithmetic."}

    errors = validate_question_data(q, ans, soln)
    assert len(errors) == 0

    # Invalid MCQ (missing question text)
    q_invalid = q.copy()
    q_invalid["question"] = ""
    errors = validate_question_data(q_invalid, ans, soln)
    assert any("question" in err for err in errors)

    # Invalid MCQ (options not list)
    q_invalid = q.copy()
    q_invalid["options"] = "not a list"
    errors = validate_question_data(q_invalid, ans, soln)
    assert any("Options must be a non-empty list" in err for err in errors)

    # Invalid MCQ (invalid correct answer)
    ans_invalid = {"id": "GCS27-PDS-E-MCQ-100", "correct_answer": "Z"}
    errors = validate_question_data(q, ans_invalid, soln)
    assert any("must be 'A', 'B', 'C', or 'D'" in err for err in errors)

    # Valid MSQ
    q_msq = q.copy()
    q_msq["type"] = "MSQ"
    ans_msq = {"id": "GCS27-PDS-E-MCQ-100", "correct_answer": '["A", "B"]'}
    errors = validate_question_data(q_msq, ans_msq, soln)
    assert len(errors) == 0
