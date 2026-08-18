import uuid
import pytest
from sqlalchemy.orm import Session

from backend.app.core.exceptions import ConflictException
from backend.app.models.content import Exam, ExamCategory
from backend.app.schemas.content import SubjectCreate, TopicCreate
from backend.app.services.content_service import ContentService
from backend.app.services.taxonomy_service import TaxonomyService


def test_subject_and_topic_uniqueness_per_exam(db_session: Session):
    service = ContentService(db_session)
    tax_service = TaxonomyService(db_session)

    cat = ExamCategory(name="SSC Exam", slug=f"s-{uuid.uuid4().hex[:6]}")
    db_session.add(cat)
    db_session.flush()

    exam = Exam(category_id=cat.id, name="SSC CGL", code=f"SSC_{uuid.uuid4().hex[:6]}")
    db_session.add(exam)
    db_session.flush()

    # Create Subject
    subj = service.create_subject(SubjectCreate(exam_id=exam.id, name="Quantitative Aptitude", code="QUANT"))
    assert subj.id is not None

    # Duplicate subject code within same exam rejected
    with pytest.raises(ConflictException):
        service.create_subject(SubjectCreate(exam_id=exam.id, name="Quant Alt", code="quant"))

    # Create Topic
    topic = service.create_topic(TopicCreate(subject_id=subj.id, name="Percentages"))
    assert topic.id is not None

    # Duplicate topic name within same subject rejected
    with pytest.raises(ConflictException):
        service.create_topic(TopicCreate(subject_id=subj.id, name=" percentages "))

    # Verify Taxonomy Tree Retrieval
    tree = tax_service.get_exam_taxonomy_tree(exam.id, active_only=True)
    assert tree.id == exam.id
    assert tree.subject_count == 1
    assert tree.subjects[0].code == "QUANT"
    assert tree.subjects[0].topics[0].name == "Percentages"
