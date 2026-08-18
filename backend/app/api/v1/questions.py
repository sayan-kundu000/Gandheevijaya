from typing import Any, List, Optional, Union

from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.orm import Session

from backend.app.api.deps import get_current_user, get_db, require_admin
from backend.app.core.security import decode_token
from backend.app.models.user import User
from backend.app.schemas.common import MessageResponse, PaginatedResponse, PaginationParams
from backend.app.schemas.content import (
    QuestionAdminResponse,
    QuestionCreate,
    QuestionStudentResponse,
    QuestionUpdate,
)
from backend.app.services.content_service import ContentService

router = APIRouter(prefix="/questions", tags=["Questions"])


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


@router.get("", response_model=PaginatedResponse[Union[QuestionStudentResponse, QuestionAdminResponse]])
def list_questions(
    topic_id: Optional[int] = Query(None, description="Filter by topic ID"),
    subtopic_id: Optional[int] = Query(None, description="Filter by subtopic ID"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty (easy, medium, hard)"),
    type: Optional[str] = Query(None, description="Filter by question type (MCQ, MSQ, NAT)"),
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status (DRAFT, REVIEW, PUBLISHED, UNPUBLISHED, ARCHIVED)"),
    search: Optional[str] = Query(None, description="Search in question text"),
    page: int = Query(1, ge=1, description="Page number starting at 1"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page (max 100)"),
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db),
):
    """
    List questions with filtering, search, and pagination.
    CRITICAL SECURITY RULE: Non-admin responses explicitly strip correct_answer and explanation.
    CRITICAL VISIBILITY RULE: Non-admin students see ONLY PUBLISHED questions under ACTIVE Exam/Subject/Topic taxonomy.
    """
    params = PaginationParams(page=page, page_size=page_size)
    service = ContentService(db)
    is_admin = current_user is not None and current_user.role == "ADMIN"

    items, total = service.get_questions(
        topic_id=topic_id,
        subtopic_id=subtopic_id,
        difficulty=difficulty,
        question_type=type,
        status=status_filter if is_admin else None,
        student_visible_only=not is_admin,
        search=search,
        skip=params.offset,
        limit=params.limit,
    )

    if is_admin:
        response_items = [QuestionAdminResponse.model_validate(q) for q in items]
    else:
        response_items = [QuestionStudentResponse.model_validate(q) for q in items]

    return PaginatedResponse.create(items=response_items, total=total, params=params)


@router.get("/{question_id}", response_model=Union[QuestionStudentResponse, QuestionAdminResponse])
def get_question(
    question_id: str,
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db),
):
    """
    Get question details by ID.
    CRITICAL SECURITY RULE: Non-admin responses explicitly strip correct_answer and explanation.
    """
    service = ContentService(db)
    question = service.get_question(question_id)

    is_admin = current_user is not None and current_user.role == "ADMIN"
    if is_admin:
        return QuestionAdminResponse.model_validate(question)
    return QuestionStudentResponse.model_validate(question)


@router.post("", response_model=QuestionAdminResponse, status_code=status.HTTP_201_CREATED)
def create_question(
    body: QuestionCreate,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Create a new question. Administrator privileges required."""
    service = ContentService(db)
    question = service.create_question(body, user_id=admin_user.id)
    return QuestionAdminResponse.model_validate(question)


@router.patch("/{question_id}", response_model=QuestionAdminResponse)
def update_question(
    question_id: str,
    body: QuestionUpdate,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Update a question. Administrator privileges required."""
    service = ContentService(db)
    question = service.update_question(question_id, body, user_id=admin_user.id)
    return QuestionAdminResponse.model_validate(question)


@router.delete("/{question_id}", response_model=MessageResponse)
def delete_question(
    question_id: str,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Delete a question. Administrator privileges required."""
    service = ContentService(db)
    service.delete_question(question_id)
    return MessageResponse(message=f"Question with ID '{question_id}' successfully deleted.")
