from fastapi import Depends

from app.ai.provider import OpenAICompatibleProvider
from app.ai.schemas import LLMProvider
from app.core.config import Settings, get_settings


def get_llm_provider(settings: Settings = Depends(get_settings)) -> LLMProvider | None:
    """Return an LLM provider only when credentials are configured.

    When no AI_API_KEY is set, this returns None and the interview engine runs
    entirely on the curated question bank. That keeps the system honest: it never
    fabricates generated questions it cannot actually produce.
    """

    if not settings.ai_is_configured:
        return None
    return OpenAICompatibleProvider(settings)
