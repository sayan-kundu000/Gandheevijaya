from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    target_exams: Optional[List[str]] = Field(default_factory=lambda: ["GATE_CS"])

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        if isinstance(v, str):
            return v.strip().lower()
        return v

    @field_validator("target_exams", mode="before")
    @classmethod
    def normalize_target_exams(cls, v: Any) -> Optional[List[str]]:
        if v is None:
            return ["GATE_CS"]
        if isinstance(v, str):
            items = [item.strip() for item in v.split(",") if item.strip()]
            return items if items else ["GATE_CS"]
        if isinstance(v, (list, tuple, set)):
            items = [str(item).strip() for item in v if str(item).strip()]
            return items if items else ["GATE_CS"]
        return ["GATE_CS"]


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters long.")

    @field_validator("password")
    @classmethod
    def validate_password_not_blank(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Password cannot be blank or contain only whitespace.")
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    @field_validator("email", mode="before")
    @classmethod
    def normalize_login_email(cls, v: str) -> str:
        if isinstance(v, str):
            return v.strip().lower()
        return v


class UserResponse(UserBase):
    id: str
    role: str
    is_active: bool
    target_exams: Optional[List[str]] = Field(default_factory=lambda: ["GATE_CS"])
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @field_validator("target_exams", mode="before")
    @classmethod
    def parse_db_target_exams(cls, v: Any) -> List[str]:
        if v is None:
            return ["GATE_CS"]
        if isinstance(v, str):
            items = [item.strip() for item in v.split(",") if item.strip()]
            return items if items else ["GATE_CS"]
        if isinstance(v, (list, tuple, set)):
            return [str(item).strip() for item in v if str(item).strip()]
        return ["GATE_CS"]


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, max_length=255)
    target_exams: Optional[List[str]] = None


class UserAdminStatusUpdate(BaseModel):
    is_active: bool


class Token(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class RefreshTokenRequest(BaseModel):
    refresh_token: Optional[str] = None


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    role: Optional[str] = None
    type: Optional[str] = None
    jti: Optional[str] = None
    family_id: Optional[str] = None


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("New password cannot be blank.")
        return v


class PasswordResetRequest(BaseModel):
    email: EmailStr

    @field_validator("email", mode="before")
    @classmethod
    def normalize_reset_email(cls, v: str) -> str:
        if isinstance(v, str):
            return v.strip().lower()
        return v


class PasswordResetConfirmRequest(BaseModel):
    token: str = Field(..., min_length=16)
    new_password: str = Field(..., min_length=8)


class GenericMessageResponse(BaseModel):
    message: str


# -----------------------------------------------------------------------------
# Question Security & Solution Protection Schemas
# -----------------------------------------------------------------------------

class QuestionForQuizStudent(BaseModel):
    """
    Sanitized question payload returned to students during active quizzes.
    Strips correct_answer, solution/explanation, and correctness metrics.
    """
    id: str
    topic_id: int
    subtopic_id: Optional[int] = None
    difficulty: str
    type: str
    question_text: str
    options: List[Dict[str, Any]]
    tags: Optional[List[str]] = None

    model_config = ConfigDict(from_attributes=True)


class QuestionForAdmin(BaseModel):
    """
    Full question model for admins or post-submission detailed review.
    Contains correct_answer and full explanation.
    """
    id: str
    topic_id: int
    subtopic_id: Optional[int] = None
    difficulty: str
    type: str
    question_text: str
    options: List[Dict[str, Any]]
    correct_answer: str
    explanation: str
    tags: Optional[List[str]] = None

    model_config = ConfigDict(from_attributes=True)
