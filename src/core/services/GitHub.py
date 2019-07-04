from dataclasses import dataclass
from hashlib import sha1
from json import dumps
from os.path import abspath, expanduser
import sys
from src.core.services.base import Base


@dataclass
class GitHub(Base):
    def is_authorized(self) -> bool:
        digest = sha1(f"{self.expected_secret}{dumps(self.body)}".encode("utf-8")).hexdigest()
        signature = f"sha1={digest}"
        print(signature)
        print(self.headers[self._rewrite_header_key("X_HUB_SIGNATURE")])
        print(str(signature == self.headers[self._rewrite_header_key("X_HUB_SIGNATURE")]))
        return signature == self.headers[self._rewrite_header_key("X_HUB_SIGNATURE")]

    def main(self) -> bool:
        # Check if this is an authorized request
        # TODO Implement validation instead
        # https://developer.github.com/webhooks/securing/#validating-payloads-from-github
#        secret_key = self.body["config"]["secrets"]
#        if not self.is_authorized(secret_key):
#            return False

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
