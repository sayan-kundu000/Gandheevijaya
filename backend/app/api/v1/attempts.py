from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from backend.app.api.deps import get_current_user, get_db, require_student
from backend.app.models.user import User
from backend.app.schemas.common import MessageResponse, PaginatedResponse, PaginationParams
from backend.app.schemas.quiz import (
    AttemptAnswerResponse,
    AttemptResponse,
    AttemptResumeResponse,
    QuizSubmitRequest,
    ResultResponse,
    SingleResponseSubmitRequest,
    ToggleReviewRequest,
)
from backend.app.services.attempt_management_service import AttemptManagementService

router = APIRouter(prefix="/attempts", tags=["Attempts"])


@router.get("", response_model=PaginatedResponse[AttemptResponse])
def list_attempts(
    quiz_id: Optional[int] = Query(None, description="Filter attempts by quiz ID"),
    user_id: Optional[str] = Query(None, description="Filter attempts by user ID (Admin only)"),
    status: Optional[str] = Query(None, description="Filter by status (IN_PROGRESS, SUBMITTED, EXPIRED)"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    List quiz attempts.
    Students only see their own attempt history; Administrators can view any user's attempts.
    """
    params = PaginationParams(page=page, page_size=page_size)
    service = AttemptManagementService(db)
    items, total = service.attempt_repo.get_multi_filtered(
        db,
        user_id=current_user.id if current_user.role != "ADMIN" else user_id,
        quiz_id=quiz_id,
        status=status,
        skip=params.offset,
        limit=params.limit,
    )
    return PaginatedResponse.create(items=items, total=total, params=params)


@router.get("/{attempt_id}", response_model=AttemptResumeResponse)
def get_or_resume_attempt(
    attempt_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Resume an active attempt or view attempt details.
    Returns stored question order, answered status map, and remaining time without leaking answer keys.
    """
    service = AttemptManagementService(db)
    return service.resume_quiz_attempt(attempt_id=attempt_id, current_user=current_user)


@router.post("/{attempt_id}/responses", response_model=AttemptAnswerResponse)
def submit_single_response(
    attempt_id: str,
    body: SingleResponseSubmitRequest,
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db),
):
    """
    Submit or update a response for a single question in an active attempt.
    Validates attempt ownership, timer non-expiry, and question membership.
    """
    service = AttemptManagementService(db)
    return service.submit_single_response(attempt_id=attempt_id, payload=body, current_user=current_user)


@router.post("/{attempt_id}/questions/{question_id}/review", response_model=MessageResponse)
def toggle_review_status(
    attempt_id: str,
    question_id: str,
    body: ToggleReviewRequest,
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db),
):
    """Toggle marked_for_review status on an attempt question."""
    body.question_id = question_id
    service = AttemptManagementService(db)
    return service.toggle_review_status(attempt_id=attempt_id, payload=body, current_user=current_user)


@router.post("/{attempt_id}/submit", response_model=ResultResponse)
def submit_attempt(
    attempt_id: str,
    body: Optional[QuizSubmitRequest] = None,
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db),
):
    """
    Finalize and score a quiz attempt.
    Perform 100% server-side evaluation, score calculation, negative marking penalty, and performance metrics.
    Idempotent: Duplicate submissions return the existing finalized result.
    """
    service = AttemptManagementService(db)
    return service.submit_quiz_attempt(attempt_id=attempt_id, payload=body, current_user=current_user)
