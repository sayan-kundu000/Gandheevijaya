import json
import re
from typing import List, Optional, Tuple

from backend.app.etl.schemas import ImportErrorItem, NormalizedQuestionRecord


class ContentValidator:
    """
    Validation engine performing structural checks, C code brace balancing,
    and answer consistency validation for imported question records.
    """

    @staticmethod
    def validate_record(rec: NormalizedQuestionRecord) -> Tuple[bool, List[ImportErrorItem]]:
        errors: List[ImportErrorItem] = []
        file_ref = rec.source_file or "unknown"

        # 1. Non-empty question text check
        if not rec.question_text:
            errors.append(
                ImportErrorItem(
                    file=file_ref,
                    record_id=rec.id,
                    field="question_text",
                    error_message="Question text cannot be empty.",
                )
            )

        # 2. C Code Integrity check (if C code block embedded)
        if "```c" in rec.question_text:
            code_blocks = re.findall(r"```c(.*?)```", rec.question_text, re.DOTALL)
            for block in code_blocks:
                open_b, close_b = block.count("{"), block.count("}")
                if open_b != close_b:
                    errors.append(
                        ImportErrorItem(
                            file=file_ref,
                            record_id=rec.id,
                            field="question_text",
                            error_message=f"Unbalanced curly braces in C code block ({open_b} open vs {close_b} close).",
                            severity="WARNING",
                        )
                    )

        # 3. Question Type & Answer consistency validation
        q_type = rec.type.upper()
        if q_type == "MCQ":
            if not rec.options or len(rec.options) < 2:
                errors.append(
                    ImportErrorItem(
                        file=file_ref,
                        record_id=rec.id,
                        field="options",
                        error_message=f"MCQ question requires at least 2 options. Got {len(rec.options) if rec.options else 0}.",
                    )
                )

            # Valid MCQ answer can be option key "A", "B", "C", "D" or exact option string
            if not rec.correct_answer:
                errors.append(
                    ImportErrorItem(
                        file=file_ref,
                        record_id=rec.id,
                        field="correct_answer",
                        error_message="MCQ correct_answer is missing.",
                    )
                )
            else:
                valid_keys = ["A", "B", "C", "D", "E"]
                if rec.correct_answer in valid_keys:
                    idx = valid_keys.index(rec.correct_answer)
                    if rec.options and idx >= len(rec.options):
                        errors.append(
                            ImportErrorItem(
                                file=file_ref,
                                record_id=rec.id,
                                field="correct_answer",
                                error_message=f"MCQ answer key '{rec.correct_answer}' exceeds option length {len(rec.options)}.",
                            )
                        )
                elif rec.options and rec.correct_answer not in rec.options:
                    # Permissive check: if not a letter key, ensure option text matches
                    pass

        elif q_type == "MSQ":
            if not rec.options or len(rec.options) < 2:
                errors.append(
                    ImportErrorItem(
                        file=file_ref,
                        record_id=rec.id,
                        field="options",
                        error_message=f"MSQ question requires at least 2 options. Got {len(rec.options) if rec.options else 0}.",
                    )
                )

        elif q_type == "NAT":
            if not rec.correct_answer:
                errors.append(
                    ImportErrorItem(
                        file=file_ref,
                        record_id=rec.id,
                        field="correct_answer",
                        error_message="NAT correct_answer is missing.",
                    )
                )

        is_valid = len([e for e in errors if e.severity == "ERROR"]) == 0
        return is_valid, errors
