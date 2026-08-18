import json
import logging
import sys
from contextvars import ContextVar
from datetime import datetime, timezone
from typing import Optional

# Context variable to hold current request correlation ID across async tasks/threads
request_id_ctx_var: ContextVar[Optional[str]] = ContextVar("request_id", default=None)


class RequestIDFilter(logging.Filter):
    """Logging filter that injects the current request_id context variable into log records."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_ctx_var.get() or "N/A"
        return True


class JSONFormatter(logging.Formatter):
    """Structured JSON formatter for production log ingestion (Render/Datadog/CloudWatch)."""

    def format(self, record: logging.LogRecord) -> str:
        log_obj = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "request_id": getattr(record, "request_id", "N/A"),
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_obj)


def setup_logging(log_level: str = "INFO", is_production: bool = False) -> logging.Logger:
    """Configures structured logging format for Gandheevijaya API."""
    logger = logging.getLogger("gandheevijaya")
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # Avoid duplicate handlers if already configured
    if not logger.handlers:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, log_level.upper(), logging.INFO))
        console_handler.addFilter(RequestIDFilter())

        if is_production:
            console_handler.setFormatter(JSONFormatter())
        else:
            log_format = (
                "[%(asctime)s] [%(levelname)s] [req_id:%(request_id)s] "
                "%(name)s - %(message)s"
            )
            formatter = logging.Formatter(fmt=log_format, datefmt="%Y-%m-%d %H:%M:%S")
            console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

    return logger


logger = setup_logging()
