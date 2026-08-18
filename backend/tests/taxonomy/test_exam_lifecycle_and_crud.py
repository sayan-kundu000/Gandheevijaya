import uuid
import pytest
from sqlalchemy.orm import Session

from backend.app.core.exceptions import BadRequestException, ConflictException
from backend.app.models.content import Exam, ExamCategory
from backend.app.schemas.content import ExamCreate, ExamUpdate
from backend.app.services.content_service import ContentService


def test_exam_crud_and_code_uniqueness(db_session: Session):
    service = ContentService(db_session)
    cat = ExamCategory(name="Banking Exam", slug=f"b-{uuid.uuid4().hex[:6]}")
    db_session.add(cat)
    db_session.flush()

    code = f"BANK_PO_{uuid.uuid4().hex[:6]}"
    exam = service.create_exam(ExamCreate(category_id=cat.id, name="IBPS PO", code=code))
    assert exam.id is not None
    assert exam.code == code
    assert exam.status == "ACTIVE"

    # Duplicate code rejection
    with pytest.raises(ConflictException):
        service.create_exam(ExamCreate(category_id=cat.id, name="Duplicate PO", code=code.lower()))

    # Update exam
    updated = service.update_exam(exam.id, ExamUpdate(name="IBPS PO Updated", display_order=10))
    assert updated.name == "IBPS PO Updated"
    assert updated.display_order == 10
