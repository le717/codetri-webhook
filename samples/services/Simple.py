from src.core.services import BaseMixin


__all__ = ["Simple"]


class Simple(BaseMixin):
    def is_authorized(self) -> bool:
        """Check if this is an authorized request."""
        secret_key = self.headers.get("X-Sample-Token", "")
        return secret_key == self.secret

    def main(self) -> bool:
        # Run any required commands before we `git pull`
        if not self.run_commands(self.commands["before_pull"]):
            return False

        # Run any required commands after the `git pull`
        if not self.run_commands(self.commands["after_pull"]):
            return False

        # Everything worked! Woo! :D
        return True
