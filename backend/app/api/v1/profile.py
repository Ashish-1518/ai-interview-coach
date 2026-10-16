from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.profile import CandidateProfileCreate, CandidateProfileResponse, CandidateProfileUpdate
from app.services.profile_service import create_profile, get_profile_for_user, update_profile

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("", response_model=CandidateProfileResponse)
def read_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CandidateProfileResponse:
    profile = get_profile_for_user(db, current_user)
    if profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found.")
    return CandidateProfileResponse.model_validate(profile)


@router.post("", response_model=CandidateProfileResponse, status_code=status.HTTP_201_CREATED)
def create_candidate_profile(
    profile_in: CandidateProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CandidateProfileResponse:
    existing_profile = get_profile_for_user(db, current_user)
    if existing_profile is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Profile already exists.")
    profile = create_profile(db, current_user, profile_in)
    return CandidateProfileResponse.model_validate(profile)


@router.put("", response_model=CandidateProfileResponse)
def update_candidate_profile(
    profile_in: CandidateProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CandidateProfileResponse:
    profile = get_profile_for_user(db, current_user)
    if profile is None:
        profile = create_profile(db, current_user, CandidateProfileCreate(**profile_in.model_dump()))
    else:
        profile = update_profile(db, profile, profile_in)
    return CandidateProfileResponse.model_validate(profile)
