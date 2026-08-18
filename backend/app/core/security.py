import hashlib
import secrets
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional, Tuple, Union

import jwt
from passlib.context import CryptContext

from backend.app.core.config import settings

# Configure Argon2id password context
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain text password against a hashed password."""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    """Generate Argon2id secure hash of a plain text password."""
    return pwd_context.hash(password)


def hash_token(raw_token: str) -> str:
    """Computes a SHA-256 fingerprint hash of a token string for secure DB persistence."""
    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()


def generate_random_token(length: int = 32) -> str:
    """Generates a cryptographically random hex token string."""
    return secrets.token_hex(length)


def create_access_token(
    subject: Union[str, Any],
    role: str = "STUDENT",
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create a short-lived access JWT token."""
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    jti = str(uuid.uuid4())
    to_encode = {
        "exp": expire,
        "iat": now,
        "sub": str(subject),
        "role": role,
        "type": "access",
        "jti": jti,
    }
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def create_refresh_token(
    subject: Union[str, Any],
    family_id: Optional[str] = None,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create a long-lived refresh JWT token."""
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    jti = str(uuid.uuid4())
    token_family = family_id or str(uuid.uuid4())
    to_encode = {
        "exp": expire,
        "iat": now,
        "sub": str(subject),
        "family_id": token_family,
        "type": "refresh",
        "jti": jti,
    }
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt



def decode_token(token: str) -> Dict[str, Any]:
    """Decode a JWT token and return claims. Returns empty dict if invalid/expired."""
    try:
        return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except jwt.PyJWTError:
        return {}

