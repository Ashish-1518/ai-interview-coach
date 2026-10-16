"""Voice analysis schemas for speech metrics."""
from pydantic import BaseModel, Field

from app.nlp.text_features import TextFeatures


class VoiceAnalysisRequest(BaseModel):
    """Input payload for speech analytics."""

    transcript: str = Field(..., min_length=1, description="Transcribed audio text")
    duration_seconds: float = Field(..., gt=0.0, le=600.0, description="Audio duration in seconds")


class VoiceAnalysisResponse(BaseModel):
    """Calculated speech and pacing metrics."""

    speaking_pace_wpm: float = Field(..., ge=0.0, description="Words Per Minute")
    pace_status: str = Field(..., description="'too_slow', 'optimal', or 'too_fast'")
    estimated_pauses: int = Field(..., ge=0, description="Estimated pause count")
    clarity_score: float = Field(..., ge=0.0, le=100.0, description="Clarity rating (0-100)")
    text_features: TextFeatures
    method_map: dict[str, str] = Field(default_factory=dict)
