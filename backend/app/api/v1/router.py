from fastapi import APIRouter

from app.api.v1.analytics import router as analytics_router
from app.api.v1.auth import router as auth_router
from app.api.v1.difficulty_ml import router as ml_router
from app.api.v1.health import router as health_router
from app.api.v1.interview import router as interview_router
from app.api.v1.job_match import router as job_match_router
from app.api.v1.profile import router as profile_router
from app.api.v1.resume import router as resume_router
from app.api.v1.voice import router as voice_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(profile_router)
api_router.include_router(resume_router)
api_router.include_router(interview_router)
api_router.include_router(analytics_router)
api_router.include_router(job_match_router)
api_router.include_router(voice_router)
api_router.include_router(ml_router)
