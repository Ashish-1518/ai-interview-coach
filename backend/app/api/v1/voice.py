"""Voice analysis router."""
from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.voice import VoiceAnalysisRequest, VoiceAnalysisResponse
from app.services.voice_service import analyze_voice_transcript

router = APIRouter(prefix="/voice", tags=["voice"])


@router.post("/analyze", response_model=VoiceAnalysisResponse)
def analyze_voice(
    payload: VoiceAnalysisRequest,
    current_user: User = Depends(get_current_user),
) -> VoiceAnalysisResponse:
    """Analyze spoken answer transcript and audio duration for pace, fillers, and clarity."""
    return analyze_voice_transcript(payload)
