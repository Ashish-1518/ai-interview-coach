import logging

from app.core.config import Settings


SENSITIVE_MARKERS = ("password", "secret", "token", "api_key", "authorization")


class SecretFilter(logging.Filter):
    """Prevent obvious secret-bearing log messages from being emitted."""

    def filter(self, record: logging.LogRecord) -> bool:
        message = record.getMessage().lower()
        return not any(marker in message for marker in SENSITIVE_MARKERS)


def configure_logging(settings: Settings) -> None:
    logging.basicConfig(
        level=settings.log_level.upper(),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    logging.getLogger().addFilter(SecretFilter())
