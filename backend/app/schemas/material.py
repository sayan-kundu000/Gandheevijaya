from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from backend.app.schemas.content import SubjectResponse, SubtopicResponse, TopicResponse


class StudyMaterialBase(BaseModel):
    subject_id: int
    topic_id: Optional[int] = None
    subtopic_id: Optional[int] = None
    title: str = Field(..., max_length=255)
    content: str  # Markdown / Plain text
    media_urls: Optional[List[str]] = None


class StudyMaterialCreate(StudyMaterialBase):
    pass


class StudyMaterialUpdate(BaseModel):
    subject_id: Optional[int] = None
    topic_id: Optional[int] = None
    subtopic_id: Optional[int] = None
    title: Optional[str] = Field(None, max_length=255)
    content: Optional[str] = None
    media_urls: Optional[List[str]] = None


class StudyMaterialResponse(StudyMaterialBase):
    id: int
    created_at: datetime
    subject: Optional[SubjectResponse] = None
    topic: Optional[TopicResponse] = None
    subtopic: Optional[SubtopicResponse] = None

    model_config = ConfigDict(from_attributes=True)
