from datetime import UTC, datetime, timedelta
from typing import Any

import bcrypt
import jwt


def hash_password(password: str) -> str:
    """Hash a plaintext password with bcrypt."""

    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a plaintext password against a stored bcrypt hash."""

    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


def create_access_token(
    subject: str,
    secret_key: str,
    algorithm: str,
    expires_delta: timedelta,
) -> str:
    """Create a signed JWT access token."""

    expires_at = datetime.now(UTC) + expires_delta
    payload: dict[str, Any] = {"sub": subject, "exp": expires_at}
    return jwt.encode(payload, secret_key, algorithm=algorithm)


def decode_access_token(token: str, secret_key: str, algorithm: str) -> dict[str, Any]:
    """Decode and validate a JWT access token."""

    return jwt.decode(token, secret_key, algorithms=[algorithm])
