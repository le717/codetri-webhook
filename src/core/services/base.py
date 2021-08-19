"""
The base service that all other services inherit from.
Do not directly use this as a service!
"""

from dataclasses import dataclass, field
from subprocess import run
from typing import Any, Dict, List, Literal


@dataclass
class Base:
    name: str
    service: str
    secret: str
    branch: str
    destination: str
    before_pull: List[str]
    after_pull: List[str]
    headers: Dict[str, str] = field(default_factory=dict)
    body: Dict[str, Any] = field(default_factory=dict)

    def noop() -> Literal[True]:
        """Noop function to be used as needed by child classes."""
        return True

    def is_authorized(self) -> bool:
        raise NotImplementedError(
            "is_authorized() must be implemented by the child class!"
        )

    def run_before_pull(self) -> bool:
        raise NotImplementedError(
            "run_before_pull() must be implemented by the child class!"
        )

    def run_after_pull(self) -> bool:
        raise NotImplementedError(
            "run_after_pull() must be implemented by the child class!"
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

    def run_git_clone(self, dest_dir: str) -> bool:
        return (
            run(["git", "-C", dest_dir, "pull", "origin", self.branch]).returncode == 0
        )
