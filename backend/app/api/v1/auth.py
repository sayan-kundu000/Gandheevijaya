from typing import Optional

from fastapi import APIRouter, Depends, Request, Response, status
from sqlalchemy.orm import Session

from backend.app.api.deps import get_current_user, get_db
from backend.app.core.config import settings
from backend.app.models.user import User
from backend.app.schemas.user import (
    ChangePasswordRequest,
    GenericMessageResponse,
    PasswordResetConfirmRequest,
    PasswordResetRequest,
    RefreshTokenRequest,
    Token,
    UserCreate,
    UserLogin,
    UserResponse,
)
from backend.app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["authentication"])


def set_auth_cookies(response: Response, access_token: str, refresh_token: str, expires_in: int) -> None:
    """Helper function to set secure HttpOnly cookies for refresh token and access token."""
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        domain=settings.COOKIE_DOMAIN,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600,
    )
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        domain=settings.COOKIE_DOMAIN,
        max_age=expires_in,
    )


def clear_auth_cookies(response: Response) -> None:
    """Helper function to clear authentication cookies."""
    response.delete_cookie(key="refresh_token", domain=settings.COOKIE_DOMAIN, samesite=settings.COOKIE_SAMESITE)
    response.delete_cookie(key="access_token", domain=settings.COOKIE_DOMAIN, samesite=settings.COOKIE_SAMESITE)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new student account.
    Public self-registration ALWAYS creates a STUDENT account.
    """
    user = AuthService.register_student(db=db, user_in=user_in)
    return user


@router.post("/login", response_model=Token)
def login(
    user_in: UserLogin,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    """
    Authenticate user credentials (email & password) and issue Access JWT + Refresh Session.
    Sets HttpOnly cookies and returns token payload.
    """
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("User-Agent")

    user = AuthService.authenticate_user(
        db=db,
        email=user_in.email,
        password=user_in.password,
        ip_address=ip_address,
        user_agent=user_agent,
    )

    access_token, refresh_token, expires_in = AuthService.create_user_session(
        db=db,
        user=user,
        user_agent=user_agent,
        ip_address=ip_address,
    )

    set_auth_cookies(response, access_token=access_token, refresh_token=refresh_token, expires_in=expires_in)

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=expires_in,
        user=user,
    )


@router.post("/refresh", response_model=Token)
def refresh(
    request: Request,
    response: Response,
    body: Optional[RefreshTokenRequest] = None,
    db: Session = Depends(get_db),
):
    """
    Rotate refresh token and issue a new Access Token.
    Accepts refresh token from HttpOnly cookie or request body.
    Supports Token Reuse Detection for automatic security revocation of compromised families.
    """
    raw_refresh = request.cookies.get("refresh_token")
    if not raw_refresh and body and body.refresh_token:
        raw_refresh = body.refresh_token

    if not raw_refresh:
        return Response(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content='{"error": {"code": "UNAUTHORIZED", "message": "Refresh token is missing."}}',
            media_type="application/json",
        )

    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("User-Agent")

    new_access, new_refresh, expires_in, user = AuthService.rotate_refresh_token(
        db=db,
        raw_refresh_token=raw_refresh,
        user_agent=user_agent,
        ip_address=ip_address,
    )

    set_auth_cookies(response, access_token=new_access, refresh_token=new_refresh, expires_in=expires_in)

    return Token(
        access_token=new_access,
        refresh_token=new_refresh,
        token_type="bearer",
        expires_in=expires_in,
        user=user,
    )


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Retrieve profile data for the currently authenticated user."""
    return current_user


@router.post("/logout", response_model=GenericMessageResponse)
def logout(
    request: Request,
    response: Response,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Log out current user session and clear authentication cookies."""
    raw_refresh = request.cookies.get("refresh_token")
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("User-Agent")

    AuthService.logout_session(
        db=db,
        raw_refresh_token=raw_refresh,
        user=current_user,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    clear_auth_cookies(response)
    return GenericMessageResponse(message="Successfully logged out.")


@router.post("/logout-all", response_model=GenericMessageResponse)
def logout_all(
    request: Request,
    response: Response,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Revoke ALL active refresh sessions for the current user across all devices."""
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("User-Agent")

    AuthService.logout_all_sessions(
        db=db,
        user=current_user,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    clear_auth_cookies(response)
    return GenericMessageResponse(message="Successfully logged out of all active sessions.")


@router.post("/change-password", response_model=GenericMessageResponse)
def change_password(
    body: ChangePasswordRequest,
    request: Request,
    response: Response,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Change current user password.
    Requires current password verification and revokes all active sessions upon success.
    """
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("User-Agent")

    AuthService.change_password(
        db=db,
        user=current_user,
        current_password=body.current_password,
        new_password=body.new_password,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    clear_auth_cookies(response)
    return GenericMessageResponse(message="Password successfully changed. Please log in again with your new password.")


@router.post("/forgot-password", response_model=GenericMessageResponse)
def forgot_password(
    body: PasswordResetRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Request password reset token.
    Returns generic response to prevent account enumeration.
    """
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("User-Agent")

    msg = AuthService.request_password_reset(
        db=db,
        email=body.email,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    return GenericMessageResponse(message=msg)


@router.post("/reset-password", response_model=GenericMessageResponse)
def reset_password(
    body: PasswordResetConfirmRequest,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    """Confirm password reset using single-use reset token."""
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("User-Agent")

    AuthService.confirm_password_reset(
        db=db,
        raw_token=body.token,
        new_password=body.new_password,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    clear_auth_cookies(response)
    return GenericMessageResponse(message="Password successfully reset. Please log in with your new password.")
