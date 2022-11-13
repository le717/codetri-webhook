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


__all__ = ["Base"]


@dataclass(slots=True)
class Base:
    """Base service class. Always inherit from this class!"""

    name: str
    service: str
    secret: str
    branch: str
    destination: str
    before_pull: list[str]
    after_pull: list[str]
    headers: EnvironHeaders
    body: dict[str, Any] | None

    def is_authorized(self) -> bool:
        raise NotImplementedError(
            "is_authorized() must be implemented by the child class!"
        )

    def main(self) -> bool:
        raise NotImplementedError("main() must be implemented by the child class!")

    @staticmethod
    def run_commands(commands: list[str]) -> bool:
        success = True
        for command in commands:
            if run(command).returncode != 0:
                success = False
                break
        return success

    def pull_from_git(self, dest_dir: Path) -> bool:
        pull_command = ["git", "-C", fspath(dest_dir), "pull", "origin", self.branch]
        return run(pull_command).returncode == 0
