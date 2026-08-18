from typing import Callable

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.core.exceptions import ForbiddenException, UnauthorizedException
from backend.app.core.security import decode_token
from backend.app.models.user import User


class OAuth2PasswordBearerWithCookie(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> str:
        # Check Authorization header first, then cookie fallback
        auth_header = request.headers.get("Authorization")
        token = None
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
        elif request.cookies.get("access_token"):
            token = request.cookies.get("access_token")

        if not token:
            raise UnauthorizedException(message="Not authenticated. Please provide credentials.")
        return token


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/api/v1/auth/login")


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    """
    Validates the current access token against JWT claims and PostgreSQL database state.
    Enforces account active status (`user.is_active`).
    """
    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise UnauthorizedException(message="Could not validate credentials or access token expired.")

    user_id: str = payload.get("sub")
    if not user_id:
        raise UnauthorizedException(message="Could not validate credentials.")

    user = db.get(User, user_id)
    if not user:
        raise UnauthorizedException(message="User not found.")

    if not user.is_active:
        raise UnauthorizedException(message="User account is disabled.")

    return user


def require_authenticated_user(current_user: User = Depends(get_current_user)) -> User:
    """Dependency asserting that a valid, active user is authenticated."""
    return current_user


def require_student(current_user: User = Depends(get_current_user)) -> User:
    """Dependency asserting that the authenticated user is a STUDENT or ADMIN."""
    if current_user.role not in ("STUDENT", "ADMIN"):
        raise ForbiddenException(message="Access restricted to registered students or administrators.")
    return current_user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Dependency asserting that the authenticated user possesses the ADMIN role."""
    if current_user.role != "ADMIN":
        raise ForbiddenException(message="Insufficient privileges. Administrator role required.")
    return current_user


def verify_owner_or_admin(resource_user_id: str, current_user: User) -> bool:
    """
    Reusable ownership helper protecting against Insecure Direct Object Reference (IDOR) attacks.
    Permits access if current_user owns the resource or is an ADMIN; otherwise raises ForbiddenException.
    """
    if current_user.role == "ADMIN" or str(current_user.id) == str(resource_user_id):
        return True
    raise ForbiddenException(message="Access denied. You do not own this resource.")
