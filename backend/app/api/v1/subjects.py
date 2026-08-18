from typing import Optional

from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.orm import Session

from backend.app.api.deps import get_db, require_admin
from backend.app.core.security import decode_token
from backend.app.models.user import User
from backend.app.schemas.common import MessageResponse, PaginatedResponse, PaginationParams
from backend.app.schemas.content import (
    SubjectCreate,
    SubjectResponse,
    SubjectStatisticsResponse,
    SubjectUpdate,
)
from backend.app.services.content_service import ContentService
from backend.app.services.taxonomy_service import TaxonomyService

router = APIRouter(prefix="/subjects", tags=["Subjects"])


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


@router.get("", response_model=PaginatedResponse[SubjectResponse])
def list_subjects(
    exam_id: Optional[int] = Query(None, description="Filter subjects by exam ID"),
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status (DRAFT, ACTIVE, INACTIVE, ARCHIVED)"),
    search: Optional[str] = Query(None, description="Search subject name or code"),
    page: int = Query(1, ge=1, description="Page number starting at 1"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page (max 100)"),
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db),
):
    """List academic subjects with filtering and pagination. Students see ACTIVE subjects by default."""
    params = PaginationParams(page=page, page_size=page_size)
    service = ContentService(db)
    is_admin = current_user is not None and current_user.role == "ADMIN"
    effective_status = status_filter if is_admin else (status_filter or "ACTIVE")

    items, total = service.get_subjects(
        exam_id=exam_id, status=effective_status, search=search, skip=params.offset, limit=params.limit
    )
    return PaginatedResponse.create(items=items, total=total, params=params)


@router.get("/{subject_id}", response_model=SubjectResponse)
def get_subject(subject_id: int, db: Session = Depends(get_db)):
    """Get subject details by ID."""
    service = ContentService(db)
    return service.get_subject(subject_id)


@router.get("/{subject_id}/statistics", response_model=SubjectStatisticsResponse)
def get_subject_statistics(
    subject_id: int,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Get content statistics for a subject. Administrator privileges required."""
    service = TaxonomyService(db)
    return service.get_subject_statistics(subject_id)


@router.post("", response_model=SubjectResponse, status_code=status.HTTP_201_CREATED)
def create_subject(
    body: SubjectCreate,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Create a new subject. Administrator privileges required."""
    service = ContentService(db)
    return service.create_subject(body)


@router.patch("/{subject_id}", response_model=SubjectResponse)
def update_subject(
    subject_id: int,
    body: SubjectUpdate,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Update subject details. Administrator privileges required."""
    service = ContentService(db)
    return service.update_subject(subject_id, body)


@router.delete("/{subject_id}", response_model=MessageResponse)
def delete_subject(
    subject_id: int,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Delete a subject. Administrator privileges required."""
    service = ContentService(db)
    service.delete_subject(subject_id)
    return MessageResponse(message=f"Subject with ID {subject_id} successfully deleted.")
