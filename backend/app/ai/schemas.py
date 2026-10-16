from typing import Protocol

from pydantic import BaseModel, Field


class GeneratedQuestion(BaseModel):
    """Structured question returned by an LLM provider."""

    prompt: str = Field(min_length=10, max_length=600)
    topic: str = Field(min_length=2, max_length=120)
    difficulty: str = Field(pattern="^(beginner|intermediate|advanced)$")
    concepts: list[str] = Field(default_factory=list, max_length=8)


class LLMProvider(Protocol):
    """Interface every LLM provider must implement."""

    def generate_json(self, system_prompt: str, user_prompt: str, schema: type[BaseModel]) -> BaseModel:
        """Return a schema-validated object, or raise AIProviderError."""
