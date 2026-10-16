from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    app_name: str = "AI Interview Coach"
    app_env: str = "development"
    app_debug: bool = False
    api_v1_prefix: str = "/api/v1"
    backend_cors_origins: str = "http://localhost:5173"
    database_url: str
    log_level: str = "INFO"
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    storage_dir: str = "storage"
    max_resume_upload_size_mb: int = 5
    ai_provider: str = "openai_compatible"
    ai_base_url: str = "https://api.openai.com/v1"
    ai_api_key: str = ""
    ai_model: str = "gpt-4o-mini"
    ai_timeout_seconds: int = 30

    @property
    def effective_database_url(self) -> str:
        """Return a database URL compatible with SQLAlchemy + psycopg.

        Render provides ``postgres://…`` which SQLAlchemy 2.x doesn't accept.
        This property normalises the scheme to ``postgresql+psycopg://``.
        """
        url = self.database_url
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+psycopg://", 1)
        elif url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+psycopg://", 1)
        return url

    @property
    def max_resume_upload_size_bytes(self) -> int:
        return self.max_resume_upload_size_mb * 1024 * 1024

    @property
    def ai_is_configured(self) -> bool:
        return bool(self.ai_api_key.strip())

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.backend_cors_origins.split(",") if origin.strip()]

    model_config = SettingsConfigDict(
        env_file=("../.env", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
