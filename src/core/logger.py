import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from sys import stdout


__all__ = ["LOG", "file_handler"]


LOG = logging.getLogger("codetri-webhook")
LOG.setLevel(logging.ERROR)


def file_handler(log_name: str) -> RotatingFileHandler:
    """Create a file-based error handler."""
    handler = RotatingFileHandler(
        Path("log") / log_name,
        maxBytes=500_000,
        backupCount=5,
        delay=True,
    )
    handler.setFormatter(
        logging.Formatter("[%(asctime)s - %(levelname)s]: %(message)s")
    )
    return handler
