from typing import List, Optional, Tuple

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, selectinload

from backend.app.models.material import StudyMaterial
from backend.app.repositories.base import BaseRepository


class StudyMaterialRepository(BaseRepository[StudyMaterial]):
    def __init__(self):
        super().__init__(StudyMaterial)

    def get_multi_filtered(
        self,
        db: Session,
        subject_id: Optional[int] = None,
        topic_id: Optional[int] = None,
        subtopic_id: Optional[int] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[StudyMaterial], int]:
        stmt = select(StudyMaterial).options(
            selectinload(StudyMaterial.subject),
            selectinload(StudyMaterial.topic),
            selectinload(StudyMaterial.subtopic),
        )

        if subject_id is not None:
            stmt = stmt.where(StudyMaterial.subject_id == subject_id)
        if topic_id is not None:
            stmt = stmt.where(StudyMaterial.topic_id == topic_id)
        if subtopic_id is not None:
            stmt = stmt.where(StudyMaterial.subtopic_id == subtopic_id)
        if search:
            search_pattern = f"%{search}%"
            stmt = stmt.where(or_(StudyMaterial.title.ilike(search_pattern), StudyMaterial.content.ilike(search_pattern)))

        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = db.scalar(count_stmt) or 0

        stmt = stmt.offset(skip).limit(limit)
        items = list(db.scalars(stmt).all())
        return items, total
