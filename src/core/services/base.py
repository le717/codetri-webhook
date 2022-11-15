"""
The base service that all other services inherit from.
Do not directly use this as a service!
"""

from dataclasses import dataclass
from os import fspath
from pathlib import Path
from subprocess import run
from typing import Any

from werkzeug.datastructures import EnvironHeaders


__all__ = ["BaseMixin"]


@dataclass(slots=True)
class BaseMixin:
    """Base service mixin. Always inherit from this class!"""

    name: str
    service: str
    secret: str
    branch: str
    destination: str
    before_pull: list[list[str]]
    after_pull: list[list[str]]
    headers: EnvironHeaders
    body: dict[str, Any] | None

    def is_authorized(self) -> bool:
        raise NotImplementedError(
            "is_authorized() must be implemented by the child class!"
        )

    def main(self) -> bool:
        raise NotImplementedError("main() must be implemented by the child class!")

    def run_commands(self, commands: list[list[str]]) -> bool:
        success = True
        for command in commands:
            if run(command).returncode != 0:
                success = False
                break
        return success

    def git_pull(self, dest_dir: Path) -> bool:
        pull_command = ["git", "-C", fspath(dest_dir), "pull", "origin", self.branch]
        return run(pull_command).returncode == 0
