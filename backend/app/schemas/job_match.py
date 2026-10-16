"""Schemas for job description matching and skill gap analysis."""
from pydantic import BaseModel, Field


class JobMatchRequest(BaseModel):
    """Input payload for matching a job description against a resume."""

    jd_text: str = Field(..., min_length=20, max_length=15000, description="Raw job description text")
    resume_id: str | None = Field(None, description="Optional specific resume ID; uses latest if omitted")
    role_title: str | None = Field(None, max_length=120, description="Optional job title for context")


class SkillGapAnalysis(BaseModel):
    """Structured breakdown of matched, missing, and bonus skills."""

    matched_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    bonus_skills: list[str] = Field(default_factory=list)
    skill_match_percentage: float = Field(..., ge=0.0, le=100.0)


class JobMatchResponse(BaseModel):
    """Complete job description match result."""

    resume_id: str
    role_title: str | None = None
    extracted_jd_skills: list[str] = Field(default_factory=list)
    extracted_resume_skills: list[str] = Field(default_factory=list)
    skill_gap: SkillGapAnalysis
    semantic_similarity_score: float = Field(..., ge=0.0, le=100.0)
    overall_fit_score: float = Field(..., ge=0.0, le=100.0)
    recommendations: list[str] = Field(default_factory=list)
    method_map: dict[str, str] = Field(default_factory=dict)
