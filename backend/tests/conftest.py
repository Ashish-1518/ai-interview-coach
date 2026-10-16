import os
from collections.abc import Generator

os.environ.setdefault("DATABASE_URL", "postgresql+psycopg://test:test@localhost:5432/test")
os.environ.setdefault("APP_ENV", "test")
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key")
os.environ.setdefault("JWT_ALGORITHM", "HS256")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
os.environ.setdefault("STORAGE_DIR", "storage")
os.environ.setdefault("MAX_RESUME_UPLOAD_SIZE_MB", "5")
os.environ.setdefault("AI_API_KEY", "")
os.environ.setdefault("AI_BASE_URL", "https://api.openai.com/v1")
os.environ.setdefault("AI_MODEL", "gpt-4o-mini")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import Settings, get_settings
from app.core.database import get_db
from app.main import app
from app.models.base import Base
from app.models.candidate_profile import CandidateProfile  # noqa: F401
from app.models.evaluation import AnswerEvaluation  # noqa: F401
from app.models.interview import Interview, InterviewQuestion  # noqa: F401
from app.models.interview_answer import InterviewAnswer  # noqa: F401
from app.models.question_bank import QuestionBankItem  # noqa: F401
from app.models.resume import Resume  # noqa: F401
from app.models.user import User  # noqa: F401
from app.services.question_bank_seed import seed_question_bank


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


def override_get_settings() -> Settings:
    return Settings(
        app_name="AI Interview Coach Test",
        app_env="test",
        app_debug=False,
        api_v1_prefix="/api/v1",
        backend_cors_origins="http://localhost:5173",
        database_url="postgresql+psycopg://test:test@localhost:5432/test",
        log_level="INFO",
        jwt_secret_key="test-secret-key",
        jwt_algorithm="HS256",
        access_token_expire_minutes=60,
        storage_dir="storage",
        max_resume_upload_size_mb=5,
        ai_provider="openai_compatible",
        ai_base_url="https://api.openai.com/v1",
        ai_api_key="",
        ai_model="gpt-4o-mini",
        ai_timeout_seconds=30,
    )


@pytest.fixture
def seeded_bank(db_session: Session) -> None:
    seed_question_bank(db_session)


@pytest.fixture
def client(db_session: Session) -> Generator[TestClient, None, None]:
    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_settings] = override_get_settings
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
