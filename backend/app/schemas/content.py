from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


# -----------------------------------------------------------------------------
# Common Lifecycle & Status Schemas
# -----------------------------------------------------------------------------

class StatusUpdateRequest(BaseModel):
    status: str = Field(..., description="Target lifecycle status (e.g., DRAFT, ACTIVE, PUBLISHED, ARCHIVED)")
    comment: Optional[str] = Field(None, description="Optional administrative comment for lifecycle transition")


class BulkStatusUpdateRequest(BaseModel):
    item_ids: List[str] = Field(..., description="List of entity primary keys to update")
    status: str = Field(..., description="Target lifecycle status")


# -----------------------------------------------------------------------------
# Exam Category Schemas
# -----------------------------------------------------------------------------

class ExamCategoryBase(BaseModel):
    name: str = Field(..., max_length=255)
    slug: str = Field(..., max_length=255)


class ExamCategoryCreate(ExamCategoryBase):
    pass


class ExamCategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    slug: Optional[str] = Field(None, max_length=255)


class ExamCategoryResponse(ExamCategoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# -----------------------------------------------------------------------------
# Exam Schemas
# -----------------------------------------------------------------------------

class ExamBase(BaseModel):
    category_id: int
    name: str = Field(..., max_length=255)
    code: str = Field(..., max_length=50, description="Unique code e.g. GATE_CS, SSC_CGL, BANK_PO")
    description: Optional[str] = None
    status: str = Field(default="ACTIVE", description="DRAFT, ACTIVE, INACTIVE, ARCHIVED")
    display_order: int = Field(default=0)


class ExamCreate(ExamBase):
    pass


class ExamUpdate(BaseModel):
    category_id: Optional[int] = None
    name: Optional[str] = Field(None, max_length=255)
    code: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    status: Optional[str] = None
    display_order: Optional[int] = None


class ExamResponse(ExamBase):
    id: int
    created_at: datetime
    updated_at: datetime
    category: Optional[ExamCategoryResponse] = None

    model_config = ConfigDict(from_attributes=True)


# -----------------------------------------------------------------------------
# Subject Schemas
# -----------------------------------------------------------------------------

class SubjectBase(BaseModel):
    exam_id: int
    name: str = Field(..., max_length=255)
    code: str = Field(..., max_length=50, description="Code e.g. ALGO, CPROG, DSA, QA")
    description: Optional[str] = None
    status: str = Field(default="ACTIVE", description="DRAFT, ACTIVE, INACTIVE, ARCHIVED")
    display_order: int = Field(default=0)


class SubjectCreate(SubjectBase):
    pass


class SubjectUpdate(BaseModel):
    exam_id: Optional[int] = None
    name: Optional[str] = Field(None, max_length=255)
    code: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    status: Optional[str] = None
    display_order: Optional[int] = None


class SubjectResponse(SubjectBase):
    id: int
    created_at: datetime
    updated_at: datetime
    exam: Optional[ExamResponse] = None

    model_config = ConfigDict(from_attributes=True)


# -----------------------------------------------------------------------------
# Topic & Subtopic Schemas
# -----------------------------------------------------------------------------

class SubtopicBase(BaseModel):
    topic_id: int
    name: str = Field(..., max_length=255)


class SubtopicCreate(SubtopicBase):
    pass


class SubtopicUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)


class SubtopicResponse(SubtopicBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TopicBase(BaseModel):
    subject_id: int
    name: str = Field(..., max_length=255)
    code: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    status: str = Field(default="ACTIVE", description="DRAFT, ACTIVE, INACTIVE, ARCHIVED")
    display_order: int = Field(default=0)


class TopicCreate(TopicBase):
    pass


class TopicUpdate(BaseModel):
    subject_id: Optional[int] = None
    name: Optional[str] = Field(None, max_length=255)
    code: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    status: Optional[str] = None
    display_order: Optional[int] = None


class TopicResponse(TopicBase):
    id: int
    created_at: datetime
    updated_at: datetime
    subject: Optional[SubjectResponse] = None
    subtopics: List[SubtopicResponse] = []

    model_config = ConfigDict(from_attributes=True)


# -----------------------------------------------------------------------------
# Tree Taxonomy Browsing Schemas
# -----------------------------------------------------------------------------

class TaxonomyTreeTopic(BaseModel):
    id: int
    name: str
    code: Optional[str] = None
    status: str
    display_order: int
    question_count: int = 0
    published_question_count: int = 0
    subtopics: List[SubtopicResponse] = []


class TaxonomyTreeSubject(BaseModel):
    id: int
    name: str
    code: str
    status: str
    display_order: int
    topic_count: int = 0
    question_count: int = 0
    published_question_count: int = 0
    topics: List[TaxonomyTreeTopic] = []


class TaxonomyTreeExamResponse(BaseModel):
    id: int
    name: str
    code: str
    status: str
    display_order: int
    subject_count: int = 0
    topic_count: int = 0
    question_count: int = 0
    published_question_count: int = 0
    subjects: List[TaxonomyTreeSubject] = []


# -----------------------------------------------------------------------------
# Statistics & Health Schemas
# -----------------------------------------------------------------------------

class ExamStatisticsResponse(BaseModel):
    exam_id: int
    exam_code: str
    exam_name: str
    subject_count: int
    topic_count: int
    question_count: int
    published_question_count: int
    draft_question_count: int
    material_count: int


class SubjectStatisticsResponse(BaseModel):
    subject_id: int
    subject_code: str
    subject_name: str
    topic_count: int
    question_count: int
    published_question_count: int
    draft_question_count: int
    material_count: int


class TopicStatisticsResponse(BaseModel):
    topic_id: int
    topic_name: str
    subtopic_count: int
    question_count: int
    published_question_count: int
    draft_question_count: int


class ContentHealthIssue(BaseModel):
    type: str  # e.g., ORPHAN_QUESTION, INACTIVE_PARENT, MISSING_ANSWER, MISSING_TOPIC
    severity: str  # ERROR, WARNING
    entity_id: str
    details: str


class ContentHealthReport(BaseModel):
    generated_at: datetime
    total_exams: int
    total_subjects: int
    total_topics: int
    total_questions: int
    total_materials: int
    issue_count: int
    issues: List[ContentHealthIssue] = []


# -----------------------------------------------------------------------------
# Question Schemas (Student vs. Admin Visibility)
# -----------------------------------------------------------------------------

class QuestionBase(BaseModel):
    topic_id: int
    subtopic_id: Optional[int] = None
    difficulty: str = Field(..., description="easy, medium, hard")
    type: str = Field(..., description="MCQ, MSQ, NAT")
    question_text: str
    options: Optional[Any] = None
    tags: Optional[List[str]] = None
    status: str = Field(default="PUBLISHED", description="DRAFT, REVIEW, PUBLISHED, UNPUBLISHED, ARCHIVED")


class QuestionCreate(QuestionBase):
    id: str = Field(..., max_length=100, description="Custom unique ID e.g. GCS27-ALGO-E-MCQ-026")
    correct_answer: str
    explanation: str


class QuestionUpdate(BaseModel):
    topic_id: Optional[int] = None
    subtopic_id: Optional[int] = None
    difficulty: Optional[str] = None
    type: Optional[str] = None
    question_text: Optional[str] = None
    options: Optional[List[Any]] = None
    correct_answer: Optional[str] = None
    explanation: Optional[str] = None
    tags: Optional[List[str]] = None
    status: Optional[str] = None


class QuestionStudentResponse(QuestionBase):
    """
    Student-facing question schema.
    NEVER includes correct_answer or explanation to prevent answer leakage!
    """
    id: str
    created_at: datetime
    updated_at: datetime
    topic: Optional[TopicResponse] = None
    subtopic: Optional[SubtopicResponse] = None

    model_config = ConfigDict(from_attributes=True)


class QuestionAdminResponse(QuestionBase):
    """
    Admin-facing question schema.
    Includes full correct_answer key, explanation, and audit fields.
    """
    id: str
    correct_answer: str
    explanation: str
    source_fingerprint: Optional[str] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    topic: Optional[TopicResponse] = None
    subtopic: Optional[SubtopicResponse] = None

    model_config = ConfigDict(from_attributes=True)
