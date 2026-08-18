from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.api.deps import get_current_user, get_db
from backend.app.models.user import User
from backend.app.schemas.quiz import ResultResponse
from backend.app.services.attempt_management_service import AttemptManagementService

router = APIRouter(tags=["Results & Review"])


@router.get("/results/{attempt_id}", response_model=ResultResponse)
@router.get("/attempts/{attempt_id}/result", response_model=ResultResponse)
def get_attempt_result(
    attempt_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Retrieve full score breakdown and detailed result metrics for a finalized attempt.
    Enforces server-side IDOR ownership checks.
    """
    service = AttemptManagementService(db)
    attempt = service.attempt_repo.get_with_details(db, attempt_id=attempt_id)
    if not attempt:
        from backend.app.core.exceptions import NotFoundException
        raise NotFoundException(message=f"Attempt with ID {attempt_id} not found.")
    from backend.app.api.deps import verify_owner_or_admin
    verify_owner_or_admin(resource_user_id=attempt.user_id, current_user=current_user)
    return service._build_result_response(attempt)


@router.get("/attempts/{attempt_id}/review", response_model=ResultResponse)
def get_attempt_question_review(
    attempt_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Retrieve detailed question-by-question review (with correct answers and explanations)
    for a finalized attempt. Enforces server-side IDOR ownership checks.
    """
    service = AttemptManagementService(db)
    attempt = service.attempt_repo.get_with_details(db, attempt_id=attempt_id)
    if not attempt:
        from backend.app.core.exceptions import NotFoundException
        raise NotFoundException(message=f"Attempt with ID {attempt_id} not found.")
    from backend.app.api.deps import verify_owner_or_admin
    verify_owner_or_admin(resource_user_id=attempt.user_id, current_user=current_user)
    return service._build_result_response(attempt)
