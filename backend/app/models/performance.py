import uuid
from datetime import datetime, timezone

from sqlalchemy import JSON, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from backend.app.core.database import Base


class StudentSubjectPerformance(Base):
    __tablename__ = "student_subject_performance"

    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), primary_key=True)

    total_quizzes_taken = Column(Integer, default=0, nullable=False)
    average_score = Column(Float, default=0.0, nullable=False)
    completion_rate = Column(Float, default=0.0, nullable=False)
    last_updated = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    user = relationship("User")
    subject = relationship("Subject")


class StudentTopicPerformance(Base):
    __tablename__ = "student_topic_performance"

    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), primary_key=True)

    total_questions_attempted = Column(Integer, default=0, nullable=False)
    correct_attempts = Column(Integer, default=0, nullable=False)
    average_time_per_question = Column(Float, default=0.0, nullable=False)  # in seconds
    weakness_score = Column(Float, default=0.0, nullable=False)  # WI weakness metric
    last_updated = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    user = relationship("User")
    topic = relationship("Topic")


class PerformanceSnapshot(Base):
    __tablename__ = "performance_snapshots"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    overall_accuracy = Column(Float, default=0.0, nullable=False)
    score_trend = Column(JSON, nullable=True)  # List of floats
    weakness_summary = Column(JSON, nullable=True)  # Dict mapping topic names to accuracy

    user = relationship("User")
