from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, computed_field, field_serializer

from backend.app.schemas.content import (
    ExamResponse,
    QuestionAdminResponse,
    QuestionStudentResponse,
    SubjectResponse,
    TopicResponse,
)
from backend.app.schemas.user import UserResponse


# -----------------------------------------------------------------------------
# Quiz & QuizQuestion Schemas
# -----------------------------------------------------------------------------

class QuizQuestionAssociationInput(BaseModel):
    question_id: str
    sort_order: int = 0
    marks: float = 1.0
    negative_marks: float = 0.0


class QuizQuestionAssociationResponse(BaseModel):
    quiz_id: int
    question_id: str
    sort_order: int
    marks: float
    negative_marks: float
    question: Optional[QuestionStudentResponse] = None

    model_config = ConfigDict(from_attributes=True)


class QuizBase(BaseModel):
    subject_id: int
    exam_id: Optional[int] = None
    topic_id: Optional[int] = None
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    quiz_type: str = Field(default="PRACTICE", description="PRACTICE, TOPIC_TEST, SUBJECT_TEST, MOCK_TEST, EXAM_SIMULATION")
    status: str = Field(default="DRAFT", description="DRAFT, PUBLISHED, ARCHIVED")
    duration_minutes: int = Field(default=30, ge=1)
    passing_score: float = Field(default=0.0, ge=0.0)
    negative_marking: float = Field(default=0.25, ge=0.0)
    is_published: bool = False
    randomize_questions: bool = True
    randomize_options: bool = False
    show_solutions_after_submit: bool = True
    max_attempts: Optional[int] = None


class QuizCreate(QuizBase):
    questions: Optional[List[QuizQuestionAssociationInput]] = None


class QuizUpdate(BaseModel):
    exam_id: Optional[int] = None
    subject_id: Optional[int] = None
    topic_id: Optional[int] = None
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    quiz_type: Optional[str] = None
    status: Optional[str] = None
    duration_minutes: Optional[int] = Field(None, ge=1)
    passing_score: Optional[float] = Field(None, ge=0.0)
    negative_marking: Optional[float] = Field(None, ge=0.0)
    is_published: Optional[bool] = None
    randomize_questions: Optional[bool] = None
    randomize_options: Optional[bool] = None
    show_solutions_after_submit: Optional[bool] = None
    max_attempts: Optional[int] = None


class QuizResponse(QuizBase):
    id: int
    question_count: int = 0
    total_marks: float = 0.0
    created_by: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    exam: Optional[ExamResponse] = None
    subject: Optional[SubjectResponse] = None
    topic: Optional[TopicResponse] = None

    @computed_field
    @property
    def subject_name(self) -> Optional[str]:
        return self.subject.name if self.subject else None

    @computed_field
    @property
    def exam_name(self) -> Optional[str]:
        return self.exam.name if self.exam else None

    model_config = ConfigDict(from_attributes=True)


class QuizDetailResponse(QuizResponse):
    question_associations: List[QuizQuestionAssociationResponse] = []


class QuestionPoolInfoResponse(BaseModel):
    quiz_id: int
    exam_id: Optional[int] = None
    subject_id: int
    topic_id: Optional[int] = None
    requested_count: int
    available_published_questions: int
    has_sufficient_pool: bool
    details: Dict[str, Any] = {}


# -----------------------------------------------------------------------------
# Quiz Attempt Schemas
# -----------------------------------------------------------------------------

class SingleResponseSubmitRequest(BaseModel):
    question_id: str
    selected_answer: Optional[str] = None  # Key or JSON string or numeric value


class ToggleReviewRequest(BaseModel):
    question_id: str
    marked_for_review: bool = True


class AttemptAnswerItem(BaseModel):
    question_id: str
    selected_answer: Optional[str] = None  # Key (e.g., "opt_a", "10", etc.)


class QuizSubmitRequest(BaseModel):
    answers: Optional[List[AttemptAnswerItem]] = None


class AttemptAnswerResponse(BaseModel):
    id: str
    attempt_id: str
    question_id: str
    selected_answer: Optional[str] = None
    is_correct: bool = False
    marks_awarded: float = 0.0
    penalty_deducted: float = 0.0
    marked_for_review: bool = False
    answered_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AttemptResponse(BaseModel):
    id: str
    user_id: str
    quiz_id: int
    status: str  # IN_PROGRESS, SUBMITTED, EXPIRED
    started_at: datetime
    expires_at: datetime
    completed_at: Optional[datetime] = None
    total_questions: int = 0
    attempted_count: int = 0
    correct_count: int = 0
    incorrect_count: int = 0
    unanswered_count: int = 0
    total_marks: float = 0.0
    score: float = 0.0
    percentage: float = 0.0
    accuracy: float = 0.0
    time_taken_seconds: int = 0
    remaining_seconds: int = 0
    passed: bool = False
    question_order: Optional[List[str]] = None
    quiz: Optional[QuizResponse] = None

    @field_serializer("started_at", "expires_at", "completed_at", when_used="always")
    def serialize_datetime(self, dt: Optional[datetime]) -> Optional[str]:
        if dt is None:
            return None
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.isoformat()

    model_config = ConfigDict(from_attributes=True)


class AttemptStartResponse(BaseModel):
    attempt: AttemptResponse
    questions: List[QuestionStudentResponse]


class AttemptResumeResponse(BaseModel):
    attempt: AttemptResponse
    questions: List[QuestionStudentResponse]
    answers_map: Dict[str, Optional[str]] = {}
    review_map: Dict[str, bool] = {}


# -----------------------------------------------------------------------------
# Result / Detailed Review Schema
# -----------------------------------------------------------------------------

class QuestionReviewItem(BaseModel):
    question_id: str
    question_text: str
    options: Optional[Union[List[Any], Dict[str, Any]]] = None
    selected_answer: Optional[str] = None
    correct_answer: str
    is_correct: bool
    marks_awarded: float
    penalty_deducted: float = 0.0
    marks_possible: float
    explanation: Optional[str] = None


class ResultResponse(BaseModel):
    attempt_id: str
    quiz_id: int
    quiz_title: str
    user_id: str
    user_name: Optional[str] = None
    started_at: datetime
    completed_at: Optional[datetime] = None
    status: str = "SUBMITTED"
    total_questions: int
    attempted_count: int = 0
    correct_count: int
    incorrect_count: int
    unanswered_count: int
    total_marks: float
    score: float
    percentage: float
    accuracy: float = 0.0
    time_taken_seconds: int = 0
    passed: bool
    detailed_questions: List[QuestionReviewItem] = []
