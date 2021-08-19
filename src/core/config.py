from json import loads
from pathlib import Path
from typing import Generator


__all__ = ["hooks"]


def hooks() -> Generator[str, None, None]:
    """Load all available hook configurations."""
    for hook_file in Path("hooks").resolve().iterdir():
        yield loads(hook_file.read_text())
