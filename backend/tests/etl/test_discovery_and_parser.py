import json
import tempfile
from pathlib import Path
import pytest

from backend.app.etl.discovery import ContentDiscoverer


def test_discover_and_load_triple_pairing():
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        subj_dir = tmp_path / "cprog" / "ej"
        ques_dir = subj_dir / "quesj"
        ans_dir = subj_dir / "ansj"
        sol_dir = subj_dir / "solnj"

        ques_dir.mkdir(parents=True)
        ans_dir.mkdir(parents=True)
        sol_dir.mkdir(parents=True)

        q_file = ques_dir / "cprog01eq.json"
        a_file = ans_dir / "cprog01ea.json"
        s_file = sol_dir / "cprog01es.json"

        q_file.write_text(
            json.dumps(
                [
                    {
                        "id": "QTEST-001",
                        "subject": "PDS",
                        "topic": "Pointers",
                        "difficulty": "easy",
                        "type": "MCQ",
                        "question": "What is *p?",
                        "options": ["Val", "Addr"],
                    }
                ]
            ),
            encoding="utf-8",
        )

        a_file.write_text(
            json.dumps([{"id": "QTEST-001", "correct_answer": "A"}]), encoding="utf-8"
        )

        s_file.write_text(
            json.dumps([{"id": "QTEST-001", "explanation": "Dereference value."}]),
            encoding="utf-8",
        )

        records, errors = ContentDiscoverer.discover_and_load(str(tmp_path))
        assert len(records) == 1
        rec, _ = records[0]
        assert rec.id == "QTEST-001"
        assert rec.correct_answer == "A"
        assert rec.explanation == "Dereference value."
