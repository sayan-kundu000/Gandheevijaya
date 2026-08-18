from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from backend.app.core.database import Base


class ContentImport(Base):
    __tablename__ = "content_imports"

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(255), nullable=False)
    content_type = Column(String(50), nullable=False)  # e.g., QUESTIONS, SOLUTIONS, BATCH
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    completed_at = Column(DateTime, nullable=True)
    status = Column(String(50), default="PENDING", nullable=False)  # PENDING, SUCCESS, FAILED

    records_found = Column(Integer, default=0, nullable=False)
    records_imported = Column(Integer, default=0, nullable=False)
    records_updated = Column(Integer, default=0, nullable=False)
    records_skipped = Column(Integer, default=0, nullable=False)
    records_failed = Column(Integer, default=0, nullable=False)
    error_count = Column(Integer, default=0, nullable=False)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    errors = relationship("ContentImportError", back_populates="content_import", cascade="all, delete-orphan")


class ContentImportError(Base):
    __tablename__ = "content_import_errors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    import_id = Column(Integer, ForeignKey("content_imports.id", ondelete="CASCADE"), nullable=False)
    record_identifier = Column(String(255), nullable=True)  # e.g., Question ID
    error_type = Column(String(100), nullable=False)  # e.g., VALIDATION_ERROR, DB_ERROR
    error_message = Column(Text, nullable=False)
    raw_reference = Column(Text, nullable=True)  # Raw JSON or string reference
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    content_import = relationship("ContentImport", back_populates="errors")
