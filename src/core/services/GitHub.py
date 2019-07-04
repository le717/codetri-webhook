from dataclasses import dataclass
from hashlib import sha1
import logging
from json import dumps
from os.path import abspath, expanduser
import sys

from src.core.services.base import Base


logger = logging.getLogger("codetri-webhook")


@dataclass
class GitHub(Base):
    def is_authorized(self) -> bool:
        # Make sure this request came from GitHub
        is_github = self.headers["User-Agent"].startswith("GitHub-Hookshot/")

        digest = sha1(f"{self.expected_secret.encode('utf-8')}{dumps(self.body).encode('utf-8')}".encode('utf-8')).hexdigest()
        signature = f"sha1={digest}"
        logger.info("Expected signature")
        logger.info(self.headers[self._rewrite_header_key("X_HUB_SIGNATURE")])
        logger.info("Created signature")
        logger.info(signature)

#        logger.info(str(signature == self.headers[self._rewrite_header_key("X_HUB_SIGNATURE")]))
        return signature == self.headers[self._rewrite_header_key("X_HUB_SIGNATURE")]

    def main(self) -> bool:
        # https://developer.github.com/webhooks/securing/#validating-payloads-from-github
#        secret_key = self.body["config"]["secrets"]

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
