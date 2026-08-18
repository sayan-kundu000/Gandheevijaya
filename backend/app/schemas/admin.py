from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, EmailStr, Field


class AdminDashboardOverviewResponse(BaseModel):
    total_users: int = Field(default=0)
    total_students: int = Field(default=0)
    total_admins: int = Field(default=0)
    active_students: int = Field(default=0)
    disabled_users: int = Field(default=0)
    total_exams: int = Field(default=0)
    total_subjects: int = Field(default=0)
    total_topics: int = Field(default=0)
    total_questions: int = Field(default=0)
    published_questions: int = Field(default=0)
    draft_questions: int = Field(default=0)
    archived_questions: int = Field(default=0)
    total_quizzes: int = Field(default=0)
    published_quizzes: int = Field(default=0)
    total_attempts: int = Field(default=0)
    completed_attempts: int = Field(default=0)
    active_attempts: int = Field(default=0)
    global_average_score: float = Field(default=0.0)
    global_accuracy: float = Field(default=0.0)
    total_import_jobs: int = Field(default=0)


class AdminUserItem(BaseModel):
    id: str
    email: EmailStr
    full_name: Optional[str] = None
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    total_attempts: int = Field(default=0)
    last_activity: Optional[datetime] = None

    class Config:
        from_attributes = True


class AdminUserDetailResponse(BaseModel):
    id: str
    email: EmailStr
    full_name: Optional[str] = None
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    total_attempts: int = Field(default=0)
    completed_attempts: int = Field(default=0)
    average_score: float = Field(default=0.0)
    overall_accuracy: float = Field(default=0.0)
    last_activity: Optional[datetime] = None


class AdminUserUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    role: Optional[str] = Field(None, description="STUDENT or ADMIN")
    is_active: Optional[bool] = None


class UserStatusToggleRequest(BaseModel):
    reason: Optional[str] = Field(None, description="Optional administrative reason for account state change")


class AdminQuestionCreateRequest(BaseModel):
    topic_id: int
    difficulty: str = Field("MEDIUM", description="EASY, MEDIUM, HARD")
    type: str = Field("MCQ", description="MCQ, MSQ, NAT")
    question_text: str
    options: Optional[Dict[str, str]] = None
    correct_answer: str
    explanation: Optional[str] = None
    status: str = Field("DRAFT", description="DRAFT, PUBLISHED, ARCHIVED")


class AdminQuestionUpdateRequest(BaseModel):
    topic_id: Optional[int] = None
    difficulty: Optional[str] = None
    type: Optional[str] = None
    question_text: Optional[str] = None
    options: Optional[Dict[str, str]] = None
    correct_answer: Optional[str] = None
    explanation: Optional[str] = None
    status: Optional[str] = None


class AdminQuizCreateRequest(BaseModel):
    subject_id: int
    topic_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    duration_minutes: int = Field(30, gt=0)
    total_marks: float = Field(100.0, gt=0)
    passing_marks: float = Field(40.0, ge=0)
    randomize_questions: bool = True
    randomize_options: bool = True
    question_selection_mode: str = Field("MANUAL", description="MANUAL or AUTOMATIC")
    status: str = Field("DRAFT", description="DRAFT, PUBLISHED, ARCHIVED")
    question_ids: Optional[List[str]] = None


class AdminQuizUpdateRequest(BaseModel):
    subject_id: Optional[int] = None
    topic_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    duration_minutes: Optional[int] = None
    total_marks: Optional[float] = None
    passing_marks: Optional[float] = None
    randomize_questions: Optional[bool] = None
    randomize_options: Optional[bool] = None
    status: Optional[str] = None
    question_ids: Optional[List[str]] = None


class AdminExamCreateRequest(BaseModel):
    code: str = Field(..., description="Unique exam code, e.g. GATE_CS, SSC_CGL")
    name: str
    description: Optional[str] = None
    category_id: int
    is_active: bool = True


class AdminExamUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    is_active: Optional[bool] = None


class AdminSubjectCreateRequest(BaseModel):
    exam_id: int
    code: str
    name: str
    description: Optional[str] = None
    is_active: bool = True


class AdminSubjectUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class AdminTopicCreateRequest(BaseModel):
    subject_id: int
    code: str
    name: str
    description: Optional[str] = None
    is_active: bool = True


class AdminTopicUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class AdminAttemptItem(BaseModel):
    id: str
    user_id: str
    user_email: str
    quiz_id: int
    quiz_title: str
    status: str
    score: float
    total_marks: float
    percentage: float
    accuracy: float
    started_at: datetime
    completed_at: Optional[datetime] = None


class ContentImportErrorItem(BaseModel):
    id: int
    record_identifier: Optional[str] = None
    error_type: str
    error_message: str
    raw_reference: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ContentImportJobItem(BaseModel):
    id: int
    filename: str
    content_type: str
    status: str
    records_found: int
    records_imported: int
    records_updated: int
    records_skipped: int
    records_failed: int
    error_count: int
    started_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ContentImportJobDetailResponse(ContentImportJobItem):
    errors: List[ContentImportErrorItem] = []
