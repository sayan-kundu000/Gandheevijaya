from datetime import datetime, timezone

from sqlalchemy import JSON, Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from backend.app.core.database import Base


class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), primary_key=True)
    question_id = Column(String(100), ForeignKey("questions.id", ondelete="CASCADE"), primary_key=True)
    sort_order = Column(Integer, default=0, nullable=False)
    marks = Column(Float, default=1.0, nullable=False)
    negative_marks = Column(Float, default=0.0, nullable=False)

    quiz = relationship("Quiz", back_populates="question_associations")
    question = relationship("Question", back_populates="quiz_associations")


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    exam_id = Column(Integer, ForeignKey("exams.id", ondelete="SET NULL"), nullable=True)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="SET NULL"), nullable=True)

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    quiz_type = Column(String(50), default="PRACTICE", nullable=False)  # PRACTICE, TOPIC_TEST, SUBJECT_TEST, MOCK_TEST, EXAM_SIMULATION
    status = Column(String(50), default="DRAFT", nullable=False)  # DRAFT, PUBLISHED, ARCHIVED
    duration_minutes = Column(Integer, default=30, nullable=False)
    question_count = Column(Integer, default=0, nullable=False)
    total_marks = Column(Float, default=0.0, nullable=False)
    passing_score = Column(Float, default=0.0, nullable=False)
    negative_marking = Column(Float, default=0.25, nullable=False)
    is_published = Column(Boolean, default=False, nullable=False)
    randomize_questions = Column(Boolean, default=True, nullable=False)
    randomize_options = Column(Boolean, default=False, nullable=False)
    show_solutions_after_submit = Column(Boolean, default=True, nullable=False)
    max_attempts = Column(Integer, nullable=True)  # Null means unlimited attempts

    created_by = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False
    )

    exam = relationship("Exam")
    subject = relationship("Subject", back_populates="quizzes")
    topic = relationship("Topic")
    question_associations = relationship("QuizQuestion", back_populates="quiz", cascade="all, delete-orphan")
    attempts = relationship("Attempt", back_populates="quiz", cascade="all, delete-orphan")
