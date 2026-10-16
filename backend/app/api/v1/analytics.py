"""
Analytics and report routes.

GET /api/v1/interviews/{id}/report  — full Q&A report for one interview
GET /api/v1/analytics/summary       — cross-interview aggregates
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.report import AnalyticsSummaryResponse, InterviewReportResponse
from app.services.interview_service import get_interview_for_user
from app.services.report_service import build_analytics_summary, build_interview_report

router = APIRouter(tags=["analytics"])


@router.get(
    "/interviews/{interview_id}/report",
    response_model=InterviewReportResponse,
)
def interview_report(
    interview_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> InterviewReportResponse:
    """Return the full report for a single interview with all Q&A and evaluations."""
    interview = get_interview_for_user(db, current_user, interview_id)
    if interview is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found.",
        )
    return build_interview_report(db, interview)


@router.get(
    "/analytics/summary",
    response_model=AnalyticsSummaryResponse,
)
def analytics_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> AnalyticsSummaryResponse:
    """Return aggregated performance stats across all of the user's interviews."""
    return build_analytics_summary(db, current_user)
