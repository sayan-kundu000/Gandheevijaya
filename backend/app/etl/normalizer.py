import hashlib
from typing import Any, List, Optional

from backend.app.etl.schemas import NormalizedQuestionRecord, RawQuestionImportRecord


class ContentNormalizer:
    """
    Normalizes raw question import records without altering academic meaning,
    code syntax, or mathematical notation. Computes deterministic SHA-256 fingerprint.
    """

    @staticmethod
    def compute_fingerprint(
        question_text: str,
        options: Optional[List[Any]],
        difficulty: str,
        question_type: str,
        subject: str,
    ) -> str:
        """
        Generates a deterministic SHA-256 fingerprint hash from normalized source content.
        """
        norm_q = question_text.strip().lower()
        norm_opts = str(options or []).strip().lower()
        norm_diff = difficulty.strip().lower()
        norm_type = question_type.strip().upper()
        norm_subj = subject.strip().upper()

        raw_str = f"{norm_q}|{norm_opts}|{norm_diff}|{norm_type}|{norm_subj}"
        return hashlib.sha256(raw_str.encode("utf-8")).hexdigest()

    @staticmethod
    def normalize(raw: RawQuestionImportRecord, source_file: Optional[str] = None) -> NormalizedQuestionRecord:
        # Preserve C code blocks and internal formatting; trim only surrounding text
        question_text = raw.question.strip() if raw.question else ""

        # Normalize difficulty
        diff = (raw.difficulty or "easy").strip().lower()
        if diff not in ("easy", "medium", "hard"):
            diff = "easy"

        # Normalize question type
        q_type = (raw.type or "MCQ").strip().upper()
        if q_type not in ("MCQ", "MSQ", "NAT"):
            q_type = "MCQ"

        # Subject normalization (e.g., PDS -> CPROG / ALGO / DSA)
        subject_name = (raw.subject or "GENERAL").strip()

        # Options normalization
        options = raw.options
        if q_type == "NAT":
            options = None

        correct_ans = (raw.correct_answer or "").strip()
        explanation = (raw.explanation or "").strip()
        tags = raw.reasoning_type or raw.tags or []

        fingerprint = ContentNormalizer.compute_fingerprint(
            question_text=question_text,
            options=options,
            difficulty=diff,
            question_type=q_type,
            subject=subject_name,
        )

        return NormalizedQuestionRecord(
            id=raw.id.strip(),
            subject_code_or_name=subject_name,
            topic_name=raw.topic.strip() if raw.topic else None,
            subtopic_name=raw.subtopic.strip() if raw.subtopic else None,
            difficulty=diff,
            type=q_type,
            question_text=question_text,
            options=options,
            correct_answer=correct_ans,
            explanation=explanation,
            tags=tags,
            source_fingerprint=fingerprint,
            source_file=source_file,
        )
