from datetime import datetime, timezone

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from backend.app.core.database import Base


class ExamCategory(Base):
    __tablename__ = "exam_categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, index=True, nullable=False)

    exams = relationship("Exam", back_populates="category", cascade="all, delete-orphan")


class Exam(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("exam_categories.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    code = Column(String(50), unique=True, index=True, nullable=False)  # e.g., GATE_CS, SSC_CGL
    description = Column(Text, nullable=True)
    status = Column(String(50), default="ACTIVE", nullable=False)  # DRAFT, ACTIVE, INACTIVE, ARCHIVED
    display_order = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False
    )

    category = relationship("ExamCategory", back_populates="exams")
    subjects = relationship("Subject", back_populates="exam", cascade="all, delete-orphan")


class Subject(Base):
    __tablename__ = "subjects"
    __table_args__ = (UniqueConstraint("exam_id", "code", name="uq_subject_exam_code"),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    exam_id = Column(Integer, ForeignKey("exams.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    code = Column(String(50), index=True, nullable=False)  # e.g., ALGO, DSA, QA, LR
    description = Column(Text, nullable=True)
    status = Column(String(50), default="ACTIVE", nullable=False)  # DRAFT, ACTIVE, INACTIVE, ARCHIVED
    display_order = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False
    )

    exam = relationship("Exam", back_populates="subjects")
    topics = relationship("Topic", back_populates="subject", cascade="all, delete-orphan")
    quizzes = relationship("Quiz", back_populates="subject", cascade="all, delete-orphan")


class Topic(Base):
    __tablename__ = "topics"
    __table_args__ = (UniqueConstraint("subject_id", "name", name="uq_topic_subject_name"),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    code = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="ACTIVE", nullable=False)  # DRAFT, ACTIVE, INACTIVE, ARCHIVED
    display_order = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False
    )

    subject = relationship("Subject", back_populates="topics")
    subtopics = relationship("Subtopic", back_populates="topic", cascade="all, delete-orphan")
    questions = relationship("Question", back_populates="topic", cascade="all, delete-orphan")


class Subtopic(Base):
    __tablename__ = "subtopics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    topic = relationship("Topic", back_populates="subtopics")
    questions = relationship("Question", back_populates="subtopic", cascade="all, delete-orphan")


class Question(Base):
    __tablename__ = "questions"
    __table_args__ = (UniqueConstraint("question_text", name="uq_questions_question_text"),)

    id = Column(String(100), primary_key=True)  # Custom unique ID like GCS27-ALGO-E-MCQ-026
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), index=True, nullable=False)
    subtopic_id = Column(Integer, ForeignKey("subtopics.id", ondelete="SET NULL"), index=True, nullable=True)

    difficulty = Column(String(50), index=True, nullable=False)  # easy, medium, hard
    type = Column(String(50), index=True, nullable=False)  # MCQ, MSQ, NAT
    question_text = Column(Text, nullable=False)
    options = Column(JSON, nullable=True)  # List of strings, or null for NAT
    correct_answer = Column(Text, nullable=False)  # Option key or JSON array for MSQ or numeric value
    explanation = Column(Text, nullable=False)
    tags = Column(JSON, nullable=True)  # List of strings (reasoning types, etc.)
    source_fingerprint = Column(String(64), index=True, nullable=True)  # SHA-256 fingerprint for deduplication
    status = Column(String(50), default="PUBLISHED", index=True, nullable=False)  # DRAFT, REVIEW, PUBLISHED, UNPUBLISHED, ARCHIVED
    created_by = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    updated_by = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False
    )

    topic = relationship("Topic", back_populates="questions")
    subtopic = relationship("Subtopic", back_populates="questions")
    quiz_associations = relationship("QuizQuestion", back_populates="question", cascade="all, delete-orphan")

