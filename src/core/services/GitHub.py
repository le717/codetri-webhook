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
    def set_body(self, data):
        self.body = data

    def is_authorized(self) -> bool:
        # Make sure this request came from GitHub
        is_github = self.headers["User-Agent"].startswith("GitHub-Hookshot/")

        secret = self.expected_secret.encode("utf-8")
        signature = hmac.new(secret, msg=self.body, digestmod=hashlib.sha1).hexdigest()

#        digest = hashlib.sha1(f"{self.expected_secret}{dumps(self.body)}".encode("utf-8")).hexdigest()
#        signature = f"sha1={digest}"
        logger.info("Expected signature")
        expected = self.headers[self._rewrite_header_key("X_HUB_SIGNATURE")][4:]
        logger.info(expected)
        logger.info("Created signature")
        logger.info(signature)
        logger.info(hmac.compare_digest(signature, expected))

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
