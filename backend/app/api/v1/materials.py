from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from backend.app.api.deps import get_db, require_admin
from backend.app.models.user import User
from backend.app.schemas.common import MessageResponse, PaginatedResponse, PaginationParams
from backend.app.schemas.material import StudyMaterialCreate, StudyMaterialResponse, StudyMaterialUpdate
from backend.app.services.material_service import StudyMaterialService

router = APIRouter(prefix="/materials", tags=["Study Materials"])


@router.get("", response_model=PaginatedResponse[StudyMaterialResponse])
def list_study_materials(
    subject_id: Optional[int] = Query(None, description="Filter by subject ID"),
    topic_id: Optional[int] = Query(None, description="Filter by topic ID"),
    subtopic_id: Optional[int] = Query(None, description="Filter by subtopic ID"),
    search: Optional[str] = Query(None, description="Search in title or content"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """List study materials (notes, guides, reference sheets) with filtering and search."""
    params = PaginationParams(page=page, page_size=page_size)
    service = StudyMaterialService(db)
    items, total = service.get_materials(
        subject_id=subject_id,
        topic_id=topic_id,
        subtopic_id=subtopic_id,
        search=search,
        skip=params.offset,
        limit=params.limit,
    )
    return PaginatedResponse.create(items=items, total=total, params=params)


@router.get("/{material_id}", response_model=StudyMaterialResponse)
def get_study_material(material_id: int, db: Session = Depends(get_db)):
    """Get study material content by ID."""
    service = StudyMaterialService(db)
    return service.get_material(material_id)


@router.post("", response_model=StudyMaterialResponse, status_code=status.HTTP_201_CREATED)
def create_study_material(
    body: StudyMaterialCreate,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Create new study material. Administrator privileges required."""
    service = StudyMaterialService(db)
    return service.create_material(body)


@router.patch("/{material_id}", response_model=StudyMaterialResponse)
def update_study_material(
    material_id: int,
    body: StudyMaterialUpdate,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Update study material. Administrator privileges required."""
    service = StudyMaterialService(db)
    return service.update_material(material_id, body)


@router.delete("/{material_id}", response_model=MessageResponse)
def delete_study_material(
    material_id: int,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Delete study material. Administrator privileges required."""
    service = StudyMaterialService(db)
    service.delete_material(material_id)
    return MessageResponse(message=f"Study material with ID {material_id} successfully deleted.")
