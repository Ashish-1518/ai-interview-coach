from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.config import Settings, get_settings
from app.core.database import get_db
from app.models.user import User
from app.schemas.resume import ResumeDetailResponse, ResumeResponse
from app.services.resume_service import ResumeUploadError, get_resume_for_user, list_resumes_for_user, save_and_parse_resume

router = APIRouter(prefix="/resumes", tags=["resumes"])


@router.post("", response_model=ResumeResponse, status_code=status.HTTP_201_CREATED)
def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    settings: Settings = Depends(get_settings),
) -> ResumeResponse:
    try:
        resume = save_and_parse_resume(db, current_user, file, settings)
    except ResumeUploadError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return ResumeResponse.model_validate(resume)


@router.get("", response_model=list[ResumeResponse])
def list_resumes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[ResumeResponse]:
    resumes = list_resumes_for_user(db, current_user)
    return [ResumeResponse.model_validate(resume) for resume in resumes]


@router.get("/{resume_id}", response_model=ResumeDetailResponse)
def read_resume(
    resume_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ResumeDetailResponse:
    resume = get_resume_for_user(db, current_user, resume_id)
    if resume is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found.")
    return ResumeDetailResponse(
        **ResumeResponse.model_validate(resume).model_dump(),
        raw_text_preview=resume.raw_text[:1000],
    )
