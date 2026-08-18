import logging
from typing import Any, Callable, TypeVar

from sqlalchemy.orm import Session

logger = logging.getLogger("gandheevijaya.service")
T = TypeVar("T")


class BaseService:
    """
    Base Service class defining business logic transaction boundaries and coordination.
    """

    def __init__(self, db: Session):
        self.db = db

    def execute_in_transaction(self, action: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """
        Executes a business action callable within an explicit database transaction boundary.
        Automatically commits on success or rolls back on exception.
        """
        try:
            result = action(*args, **kwargs)
            self.db.commit()
            return result
        except Exception as exc:
            self.db.rollback()
            logger.error(f"Service transaction failed: {exc}", exc_info=True)
            raise
