import hashlib
import hmac
from dataclasses import dataclass
from json import dumps
from os import chdir
from pathlib import Path

from src.core.services.base import Base


@dataclass
class GitHub(Base):
    def is_authorized(self) -> bool:
        # Make sure this user-agent is from from GitHub
        is_github = self.headers["User-Agent"].startswith("GitHub-Hookshot/")

        # Make sure we have the signature
        if (expected := self.headers.get("X-Hub-Signature-256")) is None:
            return False

        # Calculate the payload signature to ensure it's correct
        # https://developer.github.com/webhooks/securing/
        msg = dumps(self.body, separators=(",", ":")).encode("utf-8")
        signature = hmac.new(
            self.secret.encode("utf-8"), msg=msg, digestmod=hashlib.sha256
        ).hexdigest()
        return is_github and hmac.compare_digest(signature, expected[6:])

    def main(self) -> bool:
        # Get a full path to the destination and go to it
        dest_dir = Path(self.destination).expanduser().resolve()
        chdir(dest_dir)

        # Run any required commands before we `git pull`
        if not self.run_commands(self.before_pull):
            return False

        # Pull the latest code
        if not self.pull_from_git(dest_dir):
            return False

        # Run any required commands after pulling
        if not self.run_commands(self.after_pull):
            return False

        # Everything worked! Woo! :D
        return True
