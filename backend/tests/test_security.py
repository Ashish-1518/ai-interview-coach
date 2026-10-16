from datetime import timedelta

import jwt

from app.core.security import create_access_token, decode_access_token, hash_password, verify_password


def test_password_hash_is_not_plaintext() -> None:
    password_hash = hash_password("strongpass123")

    assert password_hash != "strongpass123"
    assert verify_password("strongpass123", password_hash)
    assert not verify_password("wrongpassword", password_hash)


def test_access_token_contains_subject() -> None:
    token = create_access_token(
        subject="user-123",
        secret_key="secret",
        algorithm="HS256",
        expires_delta=timedelta(minutes=5),
    )

    payload = decode_access_token(token, "secret", "HS256")

    assert payload["sub"] == "user-123"


def test_invalid_token_is_rejected() -> None:
    token = jwt.encode({"sub": "user-123"}, "correct-secret", algorithm="HS256")

    try:
        decode_access_token(token, "wrong-secret", "HS256")
    except jwt.InvalidTokenError:
        rejected = True
    else:
        rejected = False

    assert rejected is True
