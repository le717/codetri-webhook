from json import loads
from pathlib import Path
from typing import Any, Dict, Generator

import sys_vars


__all__ = ["app", "hooks"]


def app(env_name: str) -> Dict[str, Any]:
    """Collect the app configuration values.

    @param {str} config_file - The config file name to use.
    @return {dict} - A dictionary with all config values.
    """
    path = (Path() / "configuration" / f"{env_name}.json").resolve()
    file_content = loads(path.read_text())

    # Immediately add the app-specific values to the final values
    # because there is no need to fetch these from an outside source
    app_config: Dict[str, Any] = {}
    app_config.update(file_content["appConfig"])

    # Now fetch the system variable stored in a outside source
    # if they are defined at all
    system_vars = file_content.get("env", []) + file_content.get("secrets", [])
    for var in system_vars:
        app_config[var] = sys_vars.get(var)

    return app_config


def hooks() -> Generator[str, None, None]:
    """Load all available hook configurations."""
    for hook_file in Path("hooks").resolve().iterdir():
        yield loads(hook_file.read_text())
