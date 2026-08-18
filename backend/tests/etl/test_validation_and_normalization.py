import pytest

from backend.app.etl.normalizer import ContentNormalizer
from backend.app.etl.schemas import RawQuestionImportRecord
from backend.app.etl.validator import ContentValidator


def test_normalization_and_fingerprinting():
    raw = RawQuestionImportRecord(
        id="QTEST-002",
        subject=" PDS ",
        topic=" Recursion ",
        difficulty="EASY",
        type="mcq",
        question="  Consider function f(n)  ",
        options=["opt1", "opt2"],
        correct_answer="A",
        explanation="Recursion base case",
    )

    norm = ContentNormalizer.normalize(raw, source_file="test.json")
    assert norm.subject_code_or_name == "PDS"
    assert norm.difficulty == "easy"
    assert norm.type == "MCQ"
    assert norm.question_text == "Consider function f(n)"
    assert len(norm.source_fingerprint) == 64

    is_valid, errors = ContentValidator.validate_record(norm)
    assert is_valid is True
    assert len([e for e in errors if e.severity == "ERROR"]) == 0


def test_validation_mcq_option_bounds():
    raw = RawQuestionImportRecord(
        id="QTEST-003",
        subject="PDS",
        difficulty="easy",
        type="MCQ",
        question="Invalid MCQ question",
        options=["Single Option"],
        correct_answer="A",
    )
    norm = ContentNormalizer.normalize(raw)
    is_valid, errors = ContentValidator.validate_record(norm)
    assert is_valid is False
    assert any("at least 2 options" in e.error_message for e in errors)
