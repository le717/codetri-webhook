"""
The base service that all other services inherit from.
Do not directly use this as a service!
"""

from dataclasses import dataclass, field
from subprocess import run
from typing import Any, List, Dict


@dataclass
class Base:
    name: str
    service: str
    expected_secret: str
    expected_url: str
    branch: str
    destination: str
    before_pull: list
    after_pull: list
    headers: Dict[str, str] = field(default_factory=dict)
    body: Dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def _rewrite_header_key(key: str) -> str:
        """Rewrite HEADER_NAME format to Header-Name format if needed."""
        if "_" in key:
            key = key.replace("_", "-")
        if not key.istitle():
            key = key.title()
        return key

    def main(self) -> bool:
        raise NotImplementedError(
            "This method must be implemented by the child class!"
    )

    def confirm_url(self, given: str) -> bool:
        return given == self.expected_url

    def confirm_secret(self, given: str) -> bool:
        return given == self.expected_secret

    def is_authorized(self, secret_key: str) -> bool:
        is_expected_url = self.confirm_url(self.headers["Request-Url"])
        is_expected_secret = self.confirm_secret(secret_key))
        return is_expected_url and is_expected_secret

    @staticmethod
    def run_commands(commands: list) -> bool:
        success = True
        for command in commands:
            if run(command).returncode != 0:
                success = False
                break
        return success

    def run_git_clone(self, dest_dir) -> bool:
        return run(
            ["git", "-C", dest_dir, "pull", "origin", self.branch]
        ).returncode == 0

