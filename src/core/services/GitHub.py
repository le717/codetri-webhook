from dataclasses import dataclass
import hashlib
import hmac
import logging
from json import dumps
from os.path import abspath, expanduser

from src.core.services.base import Base


logger = logging.getLogger("codetri-webhook")


@dataclass
class GitHub(Base):
    def is_authorized(self) -> bool:
        # Make sure this user-agent is from from GitHub
        is_github = self.headers["User-Agent"].startswith("GitHub-Hookshot/")

        # Make sure we have the signature
        expected = self.headers.get("X-Hub-Signature")
        if not expected:
            return False

        # Calculate the payload signature to ensure it's correct
        # https://developer.github.com/webhooks/securing/
        msg = dumps(self.body, separators=(',', ':')).encode("utf-8")
        signature = hmac.new(
            self.secret.encode("utf-8"),
            msg=msg,
        digestmod=hashlib.sha1).hexdigest()
        return is_github and hmac.compare_digest(signature, expected[5:])

    def main(self) -> bool:
        # Run any required commands before we `git pull`
        if self.before_pull:
            before_result = self.run_commands(self.before_pull)
        if not before_result:
            return False

        # Get a full path to the destination before pulling our code
        dest_dir = abspath(expanduser(self.destination))
#        git_result = self.run_git_clone(dest_dir)
#        if not git_result:
#            return False

        # Run any required commands after the `git pull`
        if self.after_pull:
            after_result = self.run_commands(self.after_pull)
        if not after_result:
            return False

        # Everything worked! Woo! :D
        return True
