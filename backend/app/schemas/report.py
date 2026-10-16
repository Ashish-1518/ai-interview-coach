"""
Schemas for the interview report and analytics endpoints.

The report bundles every question + answer + evaluation for a single interview.
The analytics schemas aggregate stats across all interviews for a user.
"""
from datetime import datetime
from typing import Any

from pydantic import BaseModel

from app.schemas.evaluation import EvaluationResponse
from app.schemas.interview import InterviewResponse, QuestionResponse


# ---------------------------------------------------------------------------
# Per-question detail inside a report
# ---------------------------------------------------------------------------

class QuestionReportItem(BaseModel):
    """One question with its answer and evaluation (if answered)."""

    question: QuestionResponse
    answer_content: str | None = None
    answer_word_count: int | None = None
    evaluation: EvaluationResponse | None = None


# ---------------------------------------------------------------------------
# Full interview report
# ---------------------------------------------------------------------------

class InterviewReportResponse(BaseModel):
    """Complete report for one interview session."""

    interview: InterviewResponse
    items: list[QuestionReportItem]
    summary: "ReportSummary"


class ReportSummary(BaseModel):
    """Aggregate stats computed from all evaluations in this interview."""

    questions_asked: int
    questions_answered: int
    average_overall_score: float | None = None
    average_communication_score: float | None = None
    average_technical_accuracy_score: float | None = None
    average_word_count: float | None = None
    total_filler_count: int = 0
    average_filler_ratio: float | None = None
    difficulty_progression: list[str] = []
    strengths_summary: list[str] = []
    weaknesses_summary: list[str] = []


# Rebuild forward ref so InterviewReportResponse can reference ReportSummary
InterviewReportResponse.model_rebuild()


# ---------------------------------------------------------------------------
# Analytics — cross-interview aggregates
# ---------------------------------------------------------------------------

class InterviewHistoryItem(BaseModel):
    """One row in the performance history timeline."""

    interview_id: str
    role: str
    interview_type: str
    difficulty: str
    status: str
    created_at: datetime
    questions_asked: int
    questions_answered: int
    average_overall_score: float | None = None
    average_word_count: float | None = None


class AnalyticsSummaryResponse(BaseModel):
    """High-level stats across all of a user's interviews."""

    total_interviews: int
    completed_interviews: int
    total_questions_answered: int
    total_practice_time_estimate_minutes: int
    average_overall_score: float | None = None
    score_trend: list[float | None] = []
    strongest_topics: list[str] = []
    weakest_topics: list[str] = []
    difficulty_distribution: dict[str, int] = {}
    interview_type_distribution: dict[str, int] = {}
    history: list[InterviewHistoryItem] = []
