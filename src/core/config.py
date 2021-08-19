from json import loads
from pathlib import Path
from typing import Dict, Generator, Union

from dotenv import dotenv_values, find_dotenv


__all__ = ["app", "hooks"]


def app() -> Dict[str, Union[str, None]]:
    """Load the env variables from file."""
    vals = {}
    env_vals = dotenv_values(find_dotenv())
    for key, value in env_vals.items():
        vals[key] = value if value != "" else None
    return vals


def hooks() -> Generator[str, None, None]:
    """Load all available hook configurations."""
    for hook_file in Path("hooks").resolve().iterdir():
        yield loads(hook_file.read_text())
