import logging

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.core.database import check_database_connection, get_db
from app.schemas.health import HealthResponse

router = APIRouter(tags=["health"])
logger = logging.getLogger(__name__)


@router.get("/health", response_model=HealthResponse, status_code=status.HTTP_200_OK)
def health_check(
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> HealthResponse:
    database_status = "unavailable"
    try:
        check_database_connection(db)
        database_status = "available"
    except Exception:
        logger.exception("Database health check failed")

    return HealthResponse(
        status="ok" if database_status == "available" else "degraded",
        app_name=settings.app_name,
        environment=settings.app_env,
        database=database_status,
    )
