from datetime import datetime, timezone

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from backend.app.core.database import Base


class StudyMaterial(Base):
    __tablename__ = "study_materials"

    id = Column(Integer, primary_key=True, autoincrement=True)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="SET NULL"), nullable=True)
    subtopic_id = Column(Integer, ForeignKey("subtopics.id", ondelete="SET NULL"), nullable=True)

    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)  # Markdown text content
    media_urls = Column(JSON, nullable=True)  # JSON array of attachment links
    status = Column(String(50), default="PUBLISHED", nullable=False)  # DRAFT, REVIEW, PUBLISHED, UNPUBLISHED, ARCHIVED
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False
    )

    subject = relationship("Subject")
    topic = relationship("Topic")
    subtopic = relationship("Subtopic")
