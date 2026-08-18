import json
import tempfile
import uuid
from pathlib import Path
from typing import Tuple
import pytest
from sqlalchemy.orm import Session

from backend.app.etl.importer import QuestionImportService
from backend.app.models.content import Exam, ExamCategory, Question, Subject, Topic


def setup_db_subject_and_topic(db_session: Session) -> Tuple[int, int]:
    cat = ExamCategory(name="GATE", slug=f"g-{uuid.uuid4().hex[:6]}")
    db_session.add(cat)
    db_session.flush()

    exam = Exam(category_id=cat.id, name="GATE CS", code=f"GCS_{uuid.uuid4().hex[:6]}")
    db_session.add(exam)
    db_session.flush()

    subj = Subject(exam_id=exam.id, name="C Programming", code="CPROG")
    db_session.add(subj)
    db_session.flush()

    topic = Topic(subject_id=subj.id, name="Pointers")
    db_session.add(topic)
    db_session.flush()

    return subj.id, topic.id


def test_dry_run_and_idempotent_import_flow(db_session: Session):
    subj_id, topic_id = setup_db_subject_and_topic(db_session)

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        ques_dir = tmp_path / "quesj"
        ques_dir.mkdir(parents=True)

        q_file = ques_dir / "q1.json"
        q_file.write_text(
            json.dumps(
                [
                    {
                        "id": f"Q-IDEM-{uuid.uuid4().hex[:6]}",
                        "subject": "CPROG",
                        "topic": "Pointers",
                        "difficulty": "easy",
                        "type": "MCQ",
                        "question": "What is sizeof(int*)?",
                        "options": ["4 or 8 bytes", "1 byte"],
                        "correct_answer": "4 or 8 bytes",
                        "explanation": "Pointer size depends on architecture.",
                    }
                ]
            ),
            encoding="utf-8",
        )

        service = QuestionImportService(db_session)

        # 1. Dry-Run Import -> Must NOT modify DB!
        report_dry = service.run_import(source_path=str(tmp_path), is_dry_run=True)
        assert report_dry.is_dry_run is True
        assert report_dry.records_seen == 1
        assert report_dry.inserted == 1

        # 2. First Live Import -> Inserts 1 record
        report_live1 = service.run_import(source_path=str(tmp_path), is_dry_run=False)
        assert report_live1.inserted == 1
        assert report_live1.duplicates_detected == 0

        # 3. Second Live Import (Idempotency Check) -> 0 inserted, 1 skipped!
        report_live2 = service.run_import(source_path=str(tmp_path), is_dry_run=False)
        assert report_live2.inserted == 0
        assert report_live2.duplicates_detected == 1
        assert report_live2.skipped == 1
