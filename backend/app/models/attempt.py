import uuid
from datetime import datetime, timezone

from sqlalchemy import JSON, Boolean, Column, DateTime, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from backend.app.core.database import Base


class Attempt(Base):
    __tablename__ = "attempts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False)

    status = Column(String(50), default="IN_PROGRESS", nullable=False)  # IN_PROGRESS, SUBMITTED, EXPIRED
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    completed_at = Column(DateTime, nullable=True)

    total_questions = Column(Integer, default=0, nullable=False)
    attempted_count = Column(Integer, default=0, nullable=False)
    correct_count = Column(Integer, default=0, nullable=False)
    incorrect_count = Column(Integer, default=0, nullable=False)
    unanswered_count = Column(Integer, default=0, nullable=False)

    total_marks = Column(Float, default=0.0, nullable=False)
    score = Column(Float, default=0.0, nullable=False)
    percentage = Column(Float, default=0.0, nullable=False)
    accuracy = Column(Float, default=0.0, nullable=False)
    time_taken_seconds = Column(Integer, default=0, nullable=False)
    passed = Column(Boolean, default=False, nullable=False)

    question_order = Column(JSON, nullable=True)  # List of question IDs in assigned sequence
    option_mappings = Column(JSON, nullable=True)  # Dict of option mappings for randomization

    quiz = relationship("Quiz", back_populates="attempts")
    answers = relationship("AttemptAnswer", back_populates="attempt", cascade="all, delete-orphan")


class AttemptAnswer(Base):
    __tablename__ = "attempt_answers"
    __table_args__ = (UniqueConstraint("attempt_id", "question_id", name="uq_attempt_question_answer"),)

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    attempt_id = Column(String(36), ForeignKey("attempts.id", ondelete="CASCADE"), nullable=False)
    question_id = Column(String(100), ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)

    selected_answer = Column(String(255), nullable=True)  # Key or JSON list or numeric string
    is_correct = Column(Boolean, default=False, nullable=False)
    marks_awarded = Column(Float, default=0.0, nullable=False)
    penalty_deducted = Column(Float, default=0.0, nullable=False)
    marked_for_review = Column(Boolean, default=False, nullable=False)
    answered_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    attempt = relationship("Attempt", back_populates="answers")
    question = relationship("Question")
