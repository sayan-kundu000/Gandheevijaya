from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class RawQuestionImportRecord(BaseModel):
    id: str = Field(..., description="Unique record identifier")
    subject: Optional[str] = None
    topic: Optional[str] = None
    subtopic: Optional[str] = None
    difficulty: str = Field(default="easy")
    type: str = Field(default="MCQ")
    question: str = Field(..., description="Question text content")
    options: Optional[List[Any]] = None
    correct_answer: Optional[str] = None
    explanation: Optional[str] = None
    tags: Optional[List[str]] = None
    answer_id: Optional[str] = None
    pattern_type: Optional[str] = None
    reasoning_type: Optional[List[str]] = None
    representation: Optional[List[str]] = None

    model_config = ConfigDict(extra="ignore")


class NormalizedQuestionRecord(BaseModel):
    id: str
    subject_code_or_name: str
    topic_name: Optional[str] = None
    subtopic_name: Optional[str] = None
    difficulty: str  # easy, medium, hard
    type: str  # MCQ, MSQ, NAT
    question_text: str
    options: Optional[List[Any]] = None
    correct_answer: str
    explanation: str
    tags: List[str] = []
    source_fingerprint: str  # SHA-256 hash string
    source_file: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ImportErrorItem(BaseModel):
    file: str
    record_id: Optional[str] = None
    field: str
    error_message: str
    severity: str = "ERROR"  # ERROR, WARNING


class ContentImportReport(BaseModel):
    source_path: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    is_dry_run: bool = False
    files_processed: int = 0
    records_seen: int = 0
    valid_records: int = 0
    invalid_records: int = 0
    duplicates_detected: int = 0
    inserted: int = 0
    skipped: int = 0
    failed: int = 0
    errors: List[ImportErrorItem] = []
