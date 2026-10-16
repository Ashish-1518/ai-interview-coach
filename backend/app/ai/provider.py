import json
import logging

import httpx
from pydantic import BaseModel, ValidationError

from app.core.config import Settings

logger = logging.getLogger(__name__)


class AIProviderError(Exception):
    """Raised when an LLM provider fails or returns unusable output."""


class OpenAICompatibleProvider:
    """LLM provider that talks to any OpenAI-compatible chat completions endpoint."""

    def __init__(self, settings: Settings) -> None:
        self._base_url = settings.ai_base_url.rstrip("/")
        self._api_key = settings.ai_api_key
        self._model = settings.ai_model
        self._timeout = settings.ai_timeout_seconds

    def generate_json(self, system_prompt: str, user_prompt: str, schema: type[BaseModel]) -> BaseModel:
        payload = {
            "model": self._model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.4,
        }

        try:
            with httpx.Client(timeout=self._timeout) as client:
                response = client.post(
                    f"{self._base_url}/chat/completions",
                    headers={"Authorization": f"Bearer {self._api_key}"},
                    json=payload,
                )
                response.raise_for_status()
        except httpx.HTTPError as exc:
            raise AIProviderError("The AI provider could not be reached.") from exc

        content = response.json()["choices"][0]["message"]["content"]
        try:
            parsed = json.loads(content)
        except json.JSONDecodeError as exc:
            raise AIProviderError("The AI provider returned malformed JSON.") from exc

        try:
            return schema.model_validate(parsed)
        except ValidationError as exc:
            logger.warning("AI output failed schema validation: %s", exc)
            raise AIProviderError("The AI provider returned an unexpected structure.") from exc
