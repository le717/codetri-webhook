"""
The base service that all other services inherit from.
Do not directly use this as a service!
"""

from os import fspath
from pathlib import Path
from subprocess import run
from typing import Any

from werkzeug.datastructures import EnvironHeaders

from src.core.logger import logger


__all__ = ["BaseMixin"]


class BaseMixin:
    """Base service mixin. Always inherit from this class!"""

    def __init__(self, **kwargs) -> None:
        self.name: str = kwargs["name"]
        self.service: str = kwargs["service"]
        self.secret: str = kwargs["secret"]
        self.commands: dict[str, list[list[str]] | list] = kwargs["commands"]
        self.addi_info: dict[str, Any] = kwargs.get("addi_info", {})
        self.headers: EnvironHeaders = kwargs["headers"]
        self.body: Any = kwargs["body"]
        self.raw_body: bytes = kwargs["body"]

        # If we have a preprocess method, we need to call it
        if hasattr(self, "preprocess") and callable(self.preprocess):
            self.preprocess()

    def is_authorized(self) -> bool:
        """Determine if the request is authorized to be processed."""
        raise NotImplementedError("is_authorized() must be implemented by the child class!")

    def main(self) -> bool:
        raise NotImplementedError("main() must be implemented by the child class!")

    def run_command(self, command: list[str]) -> bool:
        """Execute a single command, indicating if it ran successfully."""
        logger.info(f"Running command `{''.join(command)}`")
        return run(command).returncode == 0

    def run_commands(self, commands: list[list[str]]) -> bool:
        success = True
        for command in commands:
            if not self.run_command(command):
                success = False
                break
        return success

    def git_pull(self, branch: str, dest_dir: Path) -> bool:
        pull_command = ["git", "-C", fspath(dest_dir), "pull", "origin", branch]
        return self.run_command(pull_command)
