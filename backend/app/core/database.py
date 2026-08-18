import logging
from typing import Generator, Optional, Tuple

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from backend.app.core.config import settings

logger = logging.getLogger("gandheevijaya.database")

# Database engine configuration with connection pooling & pinging
engine_kwargs = {
    "echo": settings.DEBUG and settings.APP_ENV == "development" and False,  # Keep SQL echo off by default unless explicitly needed
}

if settings.DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}
else:
    # PostgreSQL connection pool settings for production/staging
    engine_kwargs.update({
        "pool_size": 10,
        "max_overflow": 20,
        "pool_pre_ping": True,
        "pool_recycle": 1800,  # Recycle connections after 30 minutes
    })

engine = create_engine(
    settings.DATABASE_URL,
    **engine_kwargs
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency generator for database sessions in FastAPI routes.
    Ensures safe rollback on unhandled errors and closes session upon request completion.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def check_db_connected() -> Tuple[bool, Optional[str]]:
    """
    Executes a fast ping query (SELECT 1) to verify live database connectivity.
    Returns (True, None) if healthy, or (False, error_message) if connection fails.
    """
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True, None
    except SQLAlchemyError as exc:
        logger.error(f"Database readiness health check failed: {exc}")
        return False, str(exc)
    except Exception as exc:
        logger.error(f"Unexpected error during database health check: {exc}")
        return False, str(exc)
