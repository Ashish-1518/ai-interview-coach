import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, Integer, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Interview(Base):
    """One mock interview session and its configuration."""

    __tablename__ = "interviews"
    __table_args__ = (Index("ix_interviews_user_created", "user_id", "created_at"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    resume_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("resumes.id", ondelete="SET NULL"), nullable=True
    )
    role: Mapped[str] = mapped_column(String(120), nullable=False)
    interview_type: Mapped[str] = mapped_column(String(40), nullable=False)
    starting_difficulty: Mapped[str] = mapped_column(String(20), nullable=False)
    current_difficulty: Mapped[str] = mapped_column(String(20), nullable=False)
    target_question_count: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    questions = relationship(
        "InterviewQuestion",
        back_populates="interview",
        cascade="all, delete-orphan",
        order_by="InterviewQuestion.position",
    )


class InterviewQuestion(Base):
    """A single question asked within an interview session."""

    __tablename__ = "interview_questions"
    __table_args__ = (Index("ix_interview_questions_interview_position", "interview_id", "position"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    interview_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("interviews.id", ondelete="CASCADE"), nullable=False, index=True
    )
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    topic: Mapped[str] = mapped_column(String(120), nullable=False)
    difficulty: Mapped[str] = mapped_column(String(20), nullable=False)
    question_type: Mapped[str] = mapped_column(String(40), nullable=False)
    source: Mapped[str] = mapped_column(String(20), nullable=False)
    question_bank_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("question_bank.id", ondelete="SET NULL"), nullable=True
    )
    follow_up_of: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("interview_questions.id", ondelete="SET NULL"), nullable=True
    )
    concepts: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    interview = relationship("Interview", back_populates="questions")
    answer = relationship("InterviewAnswer", back_populates="question", uselist=False, cascade="all, delete-orphan")
