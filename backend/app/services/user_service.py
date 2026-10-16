from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.schemas.auth import UserCreate


class UserAlreadyExistsError(Exception):
    """Raised when a user tries to register with an existing email."""


class InvalidCredentialsError(Exception):
    """Raised when email or password authentication fails."""


def get_user_by_email(db: Session, email: str) -> User | None:
    normalized_email = email.lower()
    return db.scalar(select(User).where(User.email == normalized_email))


def get_user_by_id(db: Session, user_id: str) -> User | None:
    return db.get(User, user_id)


def create_user(db: Session, user_in: UserCreate) -> User:
    normalized_email = user_in.email.lower()
    if get_user_by_email(db, normalized_email):
        raise UserAlreadyExistsError("A user with this email already exists.")

    user = User(email=normalized_email, password_hash=hash_password(user_in.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> User:
    user = get_user_by_email(db, email)
    if user is None or not verify_password(password, user.password_hash):
        raise InvalidCredentialsError("Invalid email or password.")
    if not user.is_active:
        raise InvalidCredentialsError("User account is inactive.")
    return user
