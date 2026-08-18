from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.api.deps import get_current_user, get_db, require_admin, verify_owner_or_admin
from backend.app.core.exceptions import NotFoundException
from backend.app.models.user import User
from backend.app.schemas.user import UserAdminStatusUpdate, UserResponse, UserUpdate
from backend.app.services.auth_service import AuthService, log_security_event

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Retrieve profile details for current authenticated user."""
    return current_user


@router.patch("/me", response_model=UserResponse)
def update_current_user_profile(
    body: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update profile details for current authenticated user."""
    if body.full_name is not None:
        current_user.full_name = body.full_name
    if body.target_exams is not None:
        current_user.target_exams = ",".join(body.target_exams) if body.target_exams else "GATE_CS"
    db.commit()
    db.refresh(current_user)
    return current_user


@router.get("", response_model=List[UserResponse])
def list_users(
    skip: int = 0,
    limit: int = 100,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """List all registered users. Administrator privileges required."""
    users = db.scalars(select(User).offset(skip).limit(limit)).all()
    return users


@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(
    user_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get user details by ID.
    Enforces server-side IDOR ownership verification: Users can only view their own profile unless ADMIN.
    """
    verify_owner_or_admin(resource_user_id=user_id, current_user=current_user)
    user = db.get(User, user_id)
    if not user:
        raise NotFoundException(message=f"User with ID {user_id} not found.")
    return user


@router.patch("/{user_id}/status", response_model=UserResponse)
def update_user_status(
    user_id: str,
    body: UserAdminStatusUpdate,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """
    Enable or disable a user account (`is_active`).
    Administrator privileges required. If disabled, revokes all active sessions for the user.
    """
    user = db.get(User, user_id)
    if not user:
        raise NotFoundException(message=f"User with ID {user_id} not found.")

    user.is_active = body.is_active
    if not body.is_active:
        # Instantly invalidate all active refresh sessions for disabled account
        AuthService.logout_all_sessions(db=db, user=user)
        log_security_event(
            db=db,
            event_type="ACCOUNT_DISABLED",
            user_id=user.id,
            details={"disabled_by": admin_user.id},
        )

    db.commit()
    db.refresh(user)
    return user
