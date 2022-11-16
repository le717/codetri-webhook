from dataclasses import dataclass
from pprint import pprint

from src.core.services import BaseMixin, GitHubAuthMixin


__all__ = ["GHPushForm"]


@dataclass
class GHPushForm(GitHubAuthMixin, BaseMixin):
    is_form: bool = True

    def main(self) -> bool:
        # Nicely print the request body
        if self.body:
            pprint(self.body)
        else:
            print("No request body received")
        return True
