from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.ai.schemas import LLMProvider
from app.models.interview import Interview
from app.models.user import User
from app.schemas.interview import InterviewCreate
from app.services.question_service import NoQuestionAvailableError, build_next_question


class InterviewNotFoundError(Exception):
    """Raised when an interview does not exist for the current user."""


class InterviewStateError(Exception):
    """Raised when an action is invalid for the interview's current state."""


def list_interviews_for_user(db: Session, user: User) -> list[Interview]:
    statement = (
        select(Interview)
        .where(Interview.user_id == user.id)
        .order_by(Interview.created_at.desc())
        .options(selectinload(Interview.questions))
    )
    return list(db.scalars(statement))


def get_interview_for_user(db: Session, user: User, interview_id: str) -> Interview | None:
    statement = (
        select(Interview)
        .where(Interview.id == interview_id, Interview.user_id == user.id)
        .options(selectinload(Interview.questions))
    )
    return db.scalar(statement)


def create_interview(db: Session, user: User, interview_in: InterviewCreate) -> Interview:
    interview = Interview(
        user_id=user.id,
        resume_id=interview_in.resume_id,
        role=interview_in.role,
        interview_type=interview_in.interview_type,
        starting_difficulty=interview_in.difficulty,
        current_difficulty=interview_in.difficulty,
        target_question_count=interview_in.question_count,
        status="active",
    )
    db.add(interview)
    db.commit()
    db.refresh(interview)
    return interview


def ask_next_question(db: Session, interview: Interview, provider: LLMProvider | None):
    """Create and persist the next question for an interview."""

    if interview.status != "active":
        raise InterviewStateError("This interview is no longer active.")
    if len(interview.questions) >= interview.target_question_count:
        raise InterviewStateError("This interview has already asked all of its questions.")

    question = build_next_question(db, interview, provider)
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


def complete_interview(db: Session, interview: Interview) -> Interview:
    interview.status = "completed"
    interview.completed_at = datetime.now(UTC)
    db.commit()
    db.refresh(interview)
    return interview
