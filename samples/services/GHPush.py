from dataclasses import dataclass
from json import loads
from pprint import pprint

from src.core.services import BaseMixin, GitHubMixin


__all__ = ["GHPush"]


@dataclass
class GHPush(GitHubMixin, BaseMixin):
    def main(self) -> bool:
        # Nicely print the request body
        if self.body is not None:
            pprint(loads(self.body))
        else:
            print("No request body received")
        return True
