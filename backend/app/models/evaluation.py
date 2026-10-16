import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Float, ForeignKey, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class AnswerEvaluation(Base):
    """Scores and feedback for one interview answer.

    Every numeric score is stored alongside its method so the system never
    presents a heuristic as AI or an LLM judgment as a deterministic measurement.
    """

    __tablename__ = "answer_evaluations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    answer_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("interview_answers.id", ondelete="CASCADE"), nullable=False, unique=True, index=True
    )

    # LLM-produced scores (nullable: only present when an LLM provider is configured)
    overall_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    relevance_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    technical_accuracy_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    completeness_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    communication_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    structure_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    specificity_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    # LLM-produced text feedback
    strengths: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    weaknesses: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    suggestions: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)

    # STAR breakdown for behavioral questions (nullable)
    star_evaluation: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)

    # Deterministic NLP features (always present)
    text_features: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)

    # Method map: which system produced each score (e.g. {"overall_score": "llm", "text_features": "nlp:heuristic"})
    method_map: Mapped[dict[str, str]] = mapped_column(JSON, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    answer = relationship("InterviewAnswer", back_populates="evaluation")
