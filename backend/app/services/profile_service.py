from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.candidate_profile import CandidateProfile
from app.models.user import User
from app.schemas.profile import CandidateProfileCreate, CandidateProfileUpdate


def get_profile_for_user(db: Session, user: User) -> CandidateProfile | None:
    return db.scalar(select(CandidateProfile).where(CandidateProfile.user_id == user.id))


def create_profile(db: Session, user: User, profile_in: CandidateProfileCreate) -> CandidateProfile:
    profile = CandidateProfile(user_id=user.id, **profile_in.model_dump())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def update_profile(db: Session, profile: CandidateProfile, profile_in: CandidateProfileUpdate) -> CandidateProfile:
    update_data = profile_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)
    db.commit()
    db.refresh(profile)
    return profile
