from dataclasses import dataclass
from pprint import pprint

from src.core.services import BaseMixin, GitHubAuthMixin


__all__ = ["GHPushJSON"]


@dataclass
class GHPushJSON(GitHubAuthMixin, BaseMixin):
    is_json: bool = True

    def main(self) -> bool:
        # Nicely print the request body
        if self.body:
            pprint(self.body)
        else:
            print("No request body received")
        return True
