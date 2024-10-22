from pprint import pprint

from src.core.services import BaseMixin, GitHubAuthMixin


__all__ = ["GitHubFormData"]


class GitHubFormData(GitHubAuthMixin, BaseMixin):
    is_form: bool = True

    def main(self) -> bool:
        # Nicely print the request body
        if self.body:
            pprint(self.body)
        else:
            print("No request body received")
        return True
