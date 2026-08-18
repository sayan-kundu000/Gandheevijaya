from typing import List, Optional

from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.orm import Session

from backend.app.api.deps import get_db, require_admin
from backend.app.core.security import decode_token
from backend.app.models.user import User
from backend.app.schemas.common import MessageResponse, PaginatedResponse, PaginationParams
from backend.app.schemas.content import (
    SubtopicCreate,
    SubtopicResponse,
    SubtopicUpdate,
    TopicCreate,
    TopicResponse,
    TopicStatisticsResponse,
    TopicUpdate,
)
from backend.app.services.content_service import ContentService
from backend.app.services.taxonomy_service import TaxonomyService

router = APIRouter(tags=["Topics & Subtopics"])


def get_optional_user(request: Request, db: Session = Depends(get_db)) -> Optional[User]:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    token = auth_header.split(" ", 1)[1]
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        if user_id:
            return db.get(User, user_id)
    except Exception:
        pass
    return None


@router.get("/topics", response_model=PaginatedResponse[TopicResponse])
def list_topics(
    subject_id: Optional[int] = Query(None, description="Filter topics by subject ID"),
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status (DRAFT, ACTIVE, INACTIVE, ARCHIVED)"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db),
):
    """List topics for a subject with subtopic hierarchies. Students see ACTIVE topics by default."""
    params = PaginationParams(page=page, page_size=page_size)
    service = ContentService(db)
    is_admin = current_user is not None and current_user.role == "ADMIN"
    effective_status = status_filter if is_admin else (status_filter or "ACTIVE")

    items, total = service.get_topics(
        subject_id=subject_id, status=effective_status, skip=params.offset, limit=params.limit
    )
    return PaginatedResponse.create(items=items, total=total, params=params)


@router.get("/topics/{topic_id}", response_model=TopicResponse)
def get_topic(topic_id: int, db: Session = Depends(get_db)):
    """Get topic details by ID."""
    service = ContentService(db)
    return service.get_topic(topic_id)


@router.get("/topics/{topic_id}/statistics", response_model=TopicStatisticsResponse)
def get_topic_statistics(
    topic_id: int,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Get content statistics for a topic. Administrator privileges required."""
    service = TaxonomyService(db)
    return service.get_topic_statistics(topic_id)


@router.post("/topics", response_model=TopicResponse, status_code=status.HTTP_201_CREATED)
def create_topic(
    body: TopicCreate,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Create a new topic under a subject. Administrator privileges required."""
    service = ContentService(db)
    return service.create_topic(body)


@router.patch("/topics/{topic_id}", response_model=TopicResponse)
def update_topic(
    topic_id: int,
    body: TopicUpdate,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Update topic details. Administrator privileges required."""
    service = ContentService(db)
    return service.update_topic(topic_id, body)


@router.delete("/topics/{topic_id}", response_model=MessageResponse)
def delete_topic(
    topic_id: int,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Delete a topic. Administrator privileges required."""
    service = ContentService(db)
    service.delete_topic(topic_id)
    return MessageResponse(message=f"Topic with ID {topic_id} successfully deleted.")


@router.get("/subtopics", response_model=List[SubtopicResponse])
def list_subtopics(
    topic_id: Optional[int] = Query(None, description="Filter subtopics by topic ID"),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """List subtopics under a topic."""
    skip = (page - 1) * page_size
    service = ContentService(db)
    return service.get_subtopics(topic_id=topic_id, skip=skip, limit=page_size)


@router.post("/subtopics", response_model=SubtopicResponse, status_code=status.HTTP_201_CREATED)
def create_subtopic(
    body: SubtopicCreate,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Create a new subtopic under a topic. Administrator privileges required."""
    service = ContentService(db)
    return service.create_subtopic(body)
