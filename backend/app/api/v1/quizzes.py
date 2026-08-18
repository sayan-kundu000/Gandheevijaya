from typing import Optional

from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.orm import Session

from backend.app.api.deps import get_current_user, get_db, require_admin, require_student
from backend.app.core.security import decode_token
from backend.app.models.user import User
from backend.app.schemas.common import MessageResponse, PaginatedResponse, PaginationParams
from backend.app.schemas.quiz import (
    AttemptResponse,
    AttemptStartResponse,
    QuizCreate,
    QuizDetailResponse,
    QuizResponse,
    QuizUpdate,
)
from backend.app.services.attempt_management_service import AttemptManagementService
from backend.app.services.quiz_service import QuizService

router = APIRouter(prefix="/quizzes", tags=["Quizzes"])


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


@router.get("", response_model=PaginatedResponse[QuizResponse])
def list_quizzes(
    exam_id: Optional[int] = Query(None, description="Filter by Exam ID"),
    subject_id: Optional[int] = Query(None, description="Filter by Subject ID"),
    topic_id: Optional[int] = Query(None, description="Filter by Topic ID"),
    quiz_type: Optional[str] = Query(None, description="Filter by Quiz Type (PRACTICE, MOCK_TEST, etc.)"),
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status (DRAFT, PUBLISHED, ARCHIVED)"),
    is_published: Optional[bool] = Query(None, description="Filter published quizzes"),
    search: Optional[str] = Query(None, description="Search quizzes by title"),
    page: int = Query(1, ge=1),
    page_size: int = Query(100, ge=1, le=1000),
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db),
):
    """List available assessment quizzes."""
    params = PaginationParams(page=page, page_size=page_size)
    service = QuizService(db)

    # Students only see PUBLISHED quizzes
    if not current_user or current_user.role != "ADMIN":
        target_status = "PUBLISHED"
        target_pub = True
    else:
        target_status = status_filter
        target_pub = is_published

    items, total = service.get_quizzes(
        exam_id=exam_id,
        subject_id=subject_id,
        topic_id=topic_id,
        quiz_type=quiz_type,
        status=target_status,
        is_published=target_pub,
        search=search,
        skip=params.offset,
        limit=params.limit,
    )
    return PaginatedResponse.create(items=items, total=total, params=params)


@router.get("/{quiz_id}", response_model=QuizDetailResponse)
def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    """Get quiz details by ID."""
    service = QuizService(db)
    return service.get_quiz(quiz_id)


@router.post("/{quiz_id}/start", response_model=AttemptStartResponse, status_code=status.HTTP_201_CREATED)
@router.post("/{quiz_id}/attempts", response_model=AttemptStartResponse, status_code=status.HTTP_201_CREATED)
def start_quiz_attempt(
    quiz_id: int,
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db),
):
    """
    Start a new assessment quiz attempt.
    Selects questions, snapshots order, calculates expiration timestamp, and returns sanitized questions.
    """
    service = AttemptManagementService(db)
    attempt, questions = service.start_quiz_attempt(quiz_id=quiz_id, user=current_user)
    attempt_resp = AttemptResponse.model_validate(attempt)
    quiz = attempt.quiz or service.quiz_repo.get(db, id=attempt.quiz_id)
    duration_min = quiz.duration_minutes if quiz else 30
    attempt_resp.remaining_seconds = int(duration_min * 60)
    return AttemptStartResponse(attempt=attempt_resp, questions=questions)


@router.post("", response_model=QuizResponse, status_code=status.HTTP_201_CREATED)
def create_quiz(
    body: QuizCreate,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Create and configure a new quiz. Administrator privileges required."""
    service = QuizService(db)
    return service.create_quiz(body, creator_id=admin_user.id)


@router.patch("/{quiz_id}", response_model=QuizResponse)
def update_quiz(
    quiz_id: int,
    body: QuizUpdate,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Update quiz details and configuration. Administrator privileges required."""
    service = QuizService(db)
    return service.update_quiz(quiz_id, body)


@router.delete("/{quiz_id}", response_model=MessageResponse)
def delete_quiz(
    quiz_id: int,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Delete a quiz. Administrator privileges required."""
    service = QuizService(db)
    service.delete_quiz(quiz_id)
    return MessageResponse(message=f"Quiz with ID {quiz_id} successfully deleted.")
