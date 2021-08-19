"""
The base service that all other services inherit from.
Do not directly use this as a service!
"""

from dataclasses import dataclass, field
from os import fspath
from pathlib import Path
from subprocess import run
from typing import Any, Dict, List


@dataclass
class Base:
    __slots__ = [
        "name",
        "service",
        "secret",
        "branch",
        "destination",
        "before_pull",
        "after_pull",
    ]

    name: str
    service: str
    secret: str
    branch: str
    destination: str
    before_pull: List[str]
    after_pull: List[str]
    headers: Dict[str, str] = field(default_factory=dict)
    body: Dict[str, Any] = field(default_factory=dict)

    def is_authorized(self) -> bool:
        raise NotImplementedError(
            "is_authorized() must be implemented by the child class!"
        )

    def main(self) -> bool:
        raise NotImplementedError("main() must be implemented by the child class!")

    @staticmethod
    def run_commands(commands: List[str]) -> bool:
        success = True
        for command in commands:
            if run(command).returncode != 0:
                success = False
                break
        return success

    def pull_from_git(self, dest_dir: Path) -> bool:
        pull_command = ["git", "-C", fspath(dest_dir), "pull", "origin", self.branch]
        return run(pull_command).returncode == 0
