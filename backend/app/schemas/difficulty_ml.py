"""Schemas for ML difficulty classifier."""
from pydantic import BaseModel, Field


class DifficultyPredictRequest(BaseModel):
    """Input prompt to classify difficulty for."""

    prompt: str = Field(..., min_length=5, max_length=2000, description="Question text to classify")


class DifficultyPredictResponse(BaseModel):
    """Classification result from Scikit-Learn pipeline."""

    prompt: str
    predicted_difficulty: str = Field(..., description="'beginner', 'intermediate', or 'advanced'")
    confidence: float = Field(..., ge=0.0, le=1.0)
    class_probabilities: dict[str, float]
    method: str
