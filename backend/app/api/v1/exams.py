from typing import List, Optional

from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.orm import Session

from backend.app.api.deps import get_current_user, get_db, require_admin
from backend.app.core.security import decode_token
from backend.app.models.user import User
from backend.app.schemas.common import MessageResponse
from backend.app.schemas.content import (
    ExamCategoryCreate,
    ExamCategoryResponse,
    ExamCategoryUpdate,
    ExamCreate,
    ExamResponse,
    ExamStatisticsResponse,
    ExamUpdate,
    TaxonomyTreeExamResponse,
)
from backend.app.services.content_service import ContentService
from backend.app.services.taxonomy_service import TaxonomyService

router = APIRouter(prefix="/exams", tags=["Exams & Categories"])


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


@router.get("/categories", response_model=List[ExamCategoryResponse])
def list_exam_categories(db: Session = Depends(get_db)):
    """List all exam categories (e.g., GATE, SSC, Banking)."""
    service = ContentService(db)
    return service.get_categories()


@router.post("/categories", response_model=ExamCategoryResponse, status_code=status.HTTP_201_CREATED)
def create_exam_category(
    body: ExamCategoryCreate,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Create a new exam category. Administrator privileges required."""
    service = ContentService(db)
    return service.create_category(body)


@router.get("", response_model=List[ExamResponse])
def list_exams(
    category_id: Optional[int] = Query(None, description="Filter exams by category ID"),
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status (DRAFT, ACTIVE, INACTIVE, ARCHIVED)"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db),
):
    """List examination ecosystems (e.g., GATE CS, SSC CGL, Bank PO). Students see ACTIVE exams by default."""
    service = ContentService(db)
    is_admin = current_user is not None and current_user.role == "ADMIN"
    
    # Non-admin students see ACTIVE exams only
    effective_status = status_filter if is_admin else (status_filter or "ACTIVE")
    skip = (page - 1) * page_size
    return service.get_exams(category_id=category_id, status=effective_status, skip=skip, limit=page_size)


@router.get("/{exam_id}", response_model=ExamResponse)
def get_exam(exam_id: int, db: Session = Depends(get_db)):
    """Get exam details by ID."""
    service = ContentService(db)
    return service.get_exam(exam_id)


@router.get("/{exam_id}/taxonomy", response_model=TaxonomyTreeExamResponse)
def get_exam_taxonomy_tree(
    exam_id: int,
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db),
):
    """
    Get full hierarchical tree structure (Exam -> Subjects -> Topics) in a single request.
    Students see active taxonomy nodes only.
    """
    service = TaxonomyService(db)
    is_admin = current_user is not None and current_user.role == "ADMIN"
    return service.get_exam_taxonomy_tree(exam_id=exam_id, active_only=not is_admin)


@router.get("/{exam_id}/statistics", response_model=ExamStatisticsResponse)
def get_exam_statistics(
    exam_id: int,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Get content statistics for an exam ecosystem. Administrator privileges required."""
    service = TaxonomyService(db)
    return service.get_exam_statistics(exam_id)


@router.post("", response_model=ExamResponse, status_code=status.HTTP_201_CREATED)
def create_exam(
    body: ExamCreate,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Create a new exam ecosystem. Administrator privileges required."""
    service = ContentService(db)
    return service.create_exam(body)


@router.patch("/{exam_id}", response_model=ExamResponse)
def update_exam(
    exam_id: int,
    body: ExamUpdate,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Update exam ecosystem details. Administrator privileges required."""
    service = ContentService(db)
    return service.update_exam(exam_id, body)


@router.delete("/{exam_id}", response_model=MessageResponse)
def delete_exam(
    exam_id: int,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Delete an exam ecosystem. Administrator privileges required."""
    service = ContentService(db)
    service.delete_exam(exam_id)
    return MessageResponse(message=f"Exam with ID {exam_id} successfully deleted.")
