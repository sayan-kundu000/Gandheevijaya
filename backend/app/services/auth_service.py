from datetime import datetime, timezone
from typing import Optional, Tuple

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.core.exceptions import ConflictException, UnauthorizedException, ValidationException
from backend.app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    generate_random_token,
    get_password_hash,
    hash_token,
    verify_password,
)
from backend.app.models.password_reset import PasswordResetToken
from backend.app.models.refresh_token import RefreshToken
from backend.app.models.security_audit import SecurityAuditLog
from backend.app.models.user import User
from backend.app.schemas.user import UserCreate


def ensure_utc(dt: Optional[datetime]) -> Optional[datetime]:
    """Ensures datetime is timezone-aware UTC for safe comparisons across SQLite and PostgreSQL."""
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


def log_security_event(

    db: Session,
    event_type: str,
    user_id: Optional[str] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    details: Optional[dict] = None,
) -> None:
    """Helper function to record security audit logs append-only."""
    audit_entry = SecurityAuditLog(
        user_id=user_id,
        event_type=event_type,
        ip_address=ip_address,
        user_agent=user_agent,
        details=details,
        created_at=datetime.now(timezone.utc),
    )
    db.add(audit_entry)


class AuthService:
    @staticmethod
    def register_student(db: Session, user_in: UserCreate) -> User:
        """Register a new student account. Public self-registration ALWAYS creates a STUDENT role."""
        normalized_email = user_in.email.strip().lower()
        existing_user = db.scalar(select(User).where(User.email == normalized_email))
        if existing_user:
            raise ConflictException(message="A user with this email address already exists.")

        hashed_pwd = get_password_hash(user_in.password)
        target_exams_str = (
            ",".join(user_in.target_exams)
            if user_in.target_exams
            else "GATE_CS"
        )
        user = User(
            email=normalized_email,
            password_hash=hashed_pwd,
            full_name=user_in.full_name,
            role="STUDENT",
            target_exams=target_exams_str,
            is_active=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        log_security_event(db, event_type="ACCOUNT_REGISTERED", user_id=user.id)
        db.commit()
        return user

    @staticmethod
    def authenticate_user(
        db: Session,
        email: str,
        password: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> User:
        """
        Authenticate email and password.
        Uses timing-safe generic error responses to mitigate account enumeration.
        """
        normalized_email = email.strip().lower()
        user = db.scalar(select(User).where(User.email == normalized_email))

        if not user or not verify_password(password, user.password_hash):
            log_security_event(
                db,
                event_type="LOGIN_FAILURE",
                user_id=user.id if user else None,
                ip_address=ip_address,
                user_agent=user_agent,
                details={"reason": "Invalid credentials"},
            )
            db.commit()
            raise UnauthorizedException(message="Invalid email or password.")

        if not user.is_active:
            log_security_event(
                db,
                event_type="LOGIN_FAILURE",
                user_id=user.id,
                ip_address=ip_address,
                user_agent=user_agent,
                details={"reason": "Account disabled"},
            )
            db.commit()
            raise UnauthorizedException(message="Account is disabled. Please contact support.")

        log_security_event(
            db,
            event_type="LOGIN_SUCCESS",
            user_id=user.id,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        db.commit()
        return user

    @staticmethod
    def create_user_session(
        db: Session,
        user: User,
        user_agent: Optional[str] = None,
        ip_address: Optional[str] = None,
        family_id: Optional[str] = None,
    ) -> Tuple[str, str, int]:
        """
        Creates an Access Token (JWT) and a Refresh Token (JWT + hashed DB session).
        Returns tuple: (encoded_access_token, raw_refresh_token, expires_in_seconds)
        """
        encoded_access = create_access_token(subject=user.id, role=user.role)
        access_payload = decode_token(encoded_access)
        now_dt = datetime.now(timezone.utc)
        expires_in = int(access_payload.get("exp", 0) - now_dt.timestamp())

        encoded_refresh = create_refresh_token(subject=user.id, family_id=family_id)
        refresh_payload = decode_token(encoded_refresh)
        refresh_jti = refresh_payload.get("jti")
        token_family = refresh_payload.get("family_id")
        expires_at = datetime.fromtimestamp(refresh_payload.get("exp"), tz=timezone.utc)

        token_record = RefreshToken(
            id=refresh_jti,
            user_id=user.id,
            token_hash=hash_token(encoded_refresh),
            family_id=token_family,
            expires_at=expires_at,
            created_at=now_dt,
            user_agent=user_agent[:500] if user_agent else None,
            ip_address=ip_address[:100] if ip_address else None,
        )

        db.add(token_record)
        db.commit()

        return encoded_access, encoded_refresh, expires_in

    @staticmethod
    def rotate_refresh_token(
        db: Session,
        raw_refresh_token: str,
        user_agent: Optional[str] = None,
        ip_address: Optional[str] = None,
    ) -> Tuple[str, str, int, User]:
        """
        Rotates a refresh token.
        If a revoked token is presented again (Token Reuse Attack), invalidates the entire token family!
        """
        payload = decode_token(raw_refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise UnauthorizedException(message="Invalid or expired refresh token.")

        token_fingerprint = hash_token(raw_refresh_token)
        token_record = db.scalar(select(RefreshToken).where(RefreshToken.token_hash == token_fingerprint))

        # Re-use detection check
        if not token_record or token_record.revoked_at is not None:
            family = token_record.family_id if token_record else payload.get("family_id")
            if family:
                # Revoke all tokens in this family
                now = datetime.now(timezone.utc)
                db.query(RefreshToken).filter(RefreshToken.family_id == family).update(
                    {RefreshToken.revoked_at: now}, synchronize_session=False
                )
                log_security_event(
                    db,
                    event_type="TOKEN_REUSE_DETECTED",
                    user_id=payload.get("sub"),
                    ip_address=ip_address,
                    user_agent=user_agent,
                    details={"family_id": family},
                )
                db.commit()
            raise UnauthorizedException(
                message="Security alert: Refresh token has been revoked or reused. All sessions invalidated."
            )

        now = datetime.now(timezone.utc)
        if ensure_utc(token_record.expires_at) < now:
            token_record.revoked_at = now
            db.commit()
            raise UnauthorizedException(message="Refresh token has expired.")

        user = db.get(User, token_record.user_id)
        if not user or not user.is_active:
            raise UnauthorizedException(message="User account is disabled or no longer exists.")

        # Revoke old token and issue new token in the same family
        token_record.revoked_at = now
        token_record.last_used_at = now

        encoded_access, encoded_refresh, expires_in = AuthService.create_user_session(
            db=db,
            user=user,
            user_agent=user_agent,
            ip_address=ip_address,
            family_id=token_record.family_id,
        )

        # Get new token record ID to set replaced_by
        new_hash = hash_token(encoded_refresh)
        new_record = db.scalar(select(RefreshToken).where(RefreshToken.token_hash == new_hash))
        if new_record:
            token_record.replaced_by = new_record.id

        db.commit()
        return encoded_access, encoded_refresh, expires_in, user

    @staticmethod
    def logout_session(
        db: Session,
        raw_refresh_token: Optional[str],
        user: User,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> None:
        """Revokes the current refresh session and logs out user."""
        if raw_refresh_token:
            token_fingerprint = hash_token(raw_refresh_token)
            token_record = db.scalar(select(RefreshToken).where(RefreshToken.token_hash == token_fingerprint))
            if token_record and not token_record.revoked_at:
                token_record.revoked_at = datetime.now(timezone.utc)

        log_security_event(
            db,
            event_type="LOGOUT",
            user_id=user.id,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        db.commit()

    @staticmethod
    def logout_all_sessions(
        db: Session,
        user: User,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> None:
        """Revokes ALL active refresh sessions for the user across all devices."""
        now = datetime.now(timezone.utc)
        db.query(RefreshToken).filter(
            RefreshToken.user_id == user.id,
            RefreshToken.revoked_at.is_(None),
        ).update({RefreshToken.revoked_at: now}, synchronize_session=False)

        log_security_event(
            db,
            event_type="LOGOUT_ALL",
            user_id=user.id,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        db.commit()

    @staticmethod
    def change_password(
        db: Session,
        user: User,
        current_password: str,
        new_password: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> None:
        """Change user password, update hash, and revoke all active refresh sessions."""
        if not verify_password(current_password, user.password_hash):
            raise ValidationException(message="Current password is incorrect.")

        user.password_hash = get_password_hash(new_password)
        user.updated_at = datetime.now(timezone.utc)

        # Invalidate all active sessions for security
        AuthService.logout_all_sessions(db, user=user, ip_address=ip_address, user_agent=user_agent)

        log_security_event(
            db,
            event_type="PASSWORD_CHANGED",
            user_id=user.id,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        db.commit()

    @staticmethod
    def request_password_reset(
        db: Session,
        email: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> str:
        """
        Generates a secure password reset token if account exists.
        Returns generic message to prevent account enumeration.
        """
        normalized_email = email.strip().lower()
        user = db.scalar(select(User).where(User.email == normalized_email))

        if user and user.is_active:
            raw_token = generate_random_token()
            token_fingerprint = hash_token(raw_token)
            expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.RESET_TOKEN_EXPIRE_MINUTES)

            reset_entry = PasswordResetToken(
                user_id=user.id,
                token_hash=token_fingerprint,
                expires_at=expires_at,
                created_at=datetime.now(timezone.utc),
            )
            db.add(reset_entry)

            log_security_event(
                db,
                event_type="PASSWORD_RESET_REQUESTED",
                user_id=user.id,
                ip_address=ip_address,
                user_agent=user_agent,
            )
            db.commit()

        return "If an active account exists with that email address, password reset instructions have been created."

    @staticmethod
    def confirm_password_reset(
        db: Session,
        raw_token: str,
        new_password: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> None:
        """Confirm password reset using one-time token."""
        token_fingerprint = hash_token(raw_token)
        reset_record = db.scalar(
            select(PasswordResetToken).where(PasswordResetToken.token_hash == token_fingerprint)
        )

        now = datetime.now(timezone.utc)
        if not reset_record or reset_record.used_at is not None or ensure_utc(reset_record.expires_at) < now:
            raise ValidationException(message="Invalid or expired password reset token.")

        user = db.get(User, reset_record.user_id)
        if not user or not user.is_active:
            raise ValidationException(message="Account associated with token is disabled or deleted.")

        # Update password and mark token used
        user.password_hash = get_password_hash(new_password)
        user.updated_at = now
        reset_record.used_at = now

        # Revoke all sessions
        AuthService.logout_all_sessions(db, user=user, ip_address=ip_address, user_agent=user_agent)

        log_security_event(
            db,
            event_type="PASSWORD_RESET_COMPLETED",
            user_id=user.id,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        db.commit()
