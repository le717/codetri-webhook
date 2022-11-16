"""
The base service that all other services inherit from.
Do not directly use this as a service!
"""

from os import fspath
from pathlib import Path
from subprocess import run

from werkzeug.datastructures import EnvironHeaders


__all__ = ["BaseMixin"]


class BaseMixin:
    """Base service mixin. Always inherit from this class!"""

    def __init__(self, **kwargs):
        self.name: str = kwargs["name"]
        self.service: str = kwargs["service"]
        self.secret: str = kwargs["secret"]
        self.branch: str = kwargs["branch"]
        self.destination: str = kwargs["destination"]
        self.before_pull: list[list[str]] = kwargs["before_pull"]
        self.after_pull: list[list[str]] = kwargs["after_pull"]
        self.headers: EnvironHeaders = kwargs["headers"]
        self.body: bytes = kwargs["body"]

        # If we have a preprocess method, we need to call it
        if hasattr(self, "preprocess") and callable(self.preprocess):
            self.preprocess()

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
