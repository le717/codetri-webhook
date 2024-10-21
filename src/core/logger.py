import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


__all__ = ["logger", "file_handler"]


logger = logging.getLogger(__name__)


def file_handler(log_name: str) -> RotatingFileHandler:
    """Create a file-based error handler."""
    handler = RotatingFileHandler(
        (Path("log") / "app" / log_name).as_posix(),
        maxBytes=500_000,
        backupCount=5,
        delay=True,
    )
    handler.setLevel(logging.ERROR)
    handler.setFormatter(logging.Formatter("[%(asctime)s - %(levelname)s]: %(message)s"))
    return handler
