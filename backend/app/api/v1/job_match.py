"""Job match router."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.job_match import JobMatchRequest, JobMatchResponse
from app.services.job_match import ResumeNotFoundError, perform_job_match

router = APIRouter(prefix="/job-match", tags=["job-match"])


@router.post("", response_model=JobMatchResponse)
def match_job_description(
    payload: JobMatchRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> JobMatchResponse:
    """Analyze job description against user's resume for skill match and semantic fit."""
    try:
        return perform_job_match(db, current_user, payload)
    except ResumeNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
