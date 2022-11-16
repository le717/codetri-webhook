from dataclasses import dataclass
from json import loads
from pprint import pprint

from src.core.services import BaseMixin, GitHubAuthMixin


__all__ = ["GHPush"]


@dataclass
class GHPush(GitHubAuthMixin, BaseMixin):
    def main(self) -> bool:
        # Nicely print the request body
        if self.body:
            pprint(loads(self.body.decode()))
        else:
            print("No request body received")
        return True
