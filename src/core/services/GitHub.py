import hashlib
import hmac
from dataclasses import dataclass
from json import dumps
from os import chdir
from pathlib import Path

from src.core.services.base import Base
from src.core.logger import LOG


@dataclass
class GitHub(Base):
    """Service to respond to GitHub webhook requests."""

    def is_authorized(self) -> bool:
        # https://docs.github.com/en/developers/webhooks-and-events/webhooks/webhook-events-and-payloads#delivery-headers
        # Make sure this user-agent is from from GitHub
        is_github = self.headers["User-Agent"].startswith("GitHub-Hookshot/")
        if not is_github:
            LOG.error("This request's User-Agent is not from github.com!")
            LOG.info(f"User-Agent provided: {self.headers['User-Agent']}")

        # Make sure we have the signature
        if (expected := self.headers.get("X-Hub-Signature-256")) is None:
            LOG.error("X-Hub-Signature-256 header was not provided!")
            return False

        # Calculate the payload signature to ensure it's correct
        # https://developer.github.com/webhooks/securing/
        msg = dumps(self.body, separators=(",", ":")).encode("utf-8")
        signature = hmac.new(
            self.secret.encode("utf-8"), msg=msg, digestmod=hashlib.sha256
        ).hexdigest()
        digests_are_equal = hmac.compare_digest(signature, expected[7:])

        if not digests_are_equal:
            LOG.error("Payload signatures do not match!")
        return is_github and digests_are_equal

    def main(self) -> bool:
        # Get a full path to the destination and go to it
        dest_dir = Path(self.destination).expanduser().resolve()
        chdir(dest_dir)

        # Run any required commands before we `git pull`
        if not self.run_commands(self.before_pull):
            return False

        # Pull the latest code
        if not self.git_pull(dest_dir):
            return False

        # Run any required commands after pulling
        if not self.run_commands(self.after_pull):
            return False

        # Everything worked! Woo! :D
        return True
