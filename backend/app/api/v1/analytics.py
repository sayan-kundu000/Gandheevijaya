from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.api.deps import get_current_user, get_db, require_admin, verify_owner_or_admin
from backend.app.models.user import User
from backend.app.schemas.analytics import UserPerformanceSummary
from backend.app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Performance Analytics"])


@router.get("/me", response_model=UserPerformanceSummary)
def get_my_performance_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get aggregated performance analytics summary for the current student."""
    service = AnalyticsService(db)
    return service.get_user_performance_summary(user_id=current_user.id, user_name=current_user.full_name or "Student")


@router.get("/users/{user_id}", response_model=UserPerformanceSummary)
def get_user_performance_summary(
    user_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get aggregated performance analytics summary for a specific user.
    Enforces server-side IDOR ownership checks: Students can only view their own analytics unless ADMIN.
    """
    verify_owner_or_admin(resource_user_id=user_id, current_user=current_user)
    service = AnalyticsService(db)
    target_user = db.get(User, user_id)
    user_name = target_user.full_name if target_user else "Student"
    return service.get_user_performance_summary(user_id=user_id, user_name=user_name)
