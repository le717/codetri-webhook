from src.core.services import BaseMixin


__all__ = ["Simple"]


class Simple(BaseMixin):
    def is_authorized(self) -> bool:
        """Check if this is an authorized request."""
        # We must have an Authorization header
        if (auth_header := self.headers.get("Authorization")) is None:
            return False

        # Make sure there's two parts to the header
        parts = auth_header.split(" ")
        if len(parts) != 2 or parts[0].lower() == "bearer":
            return False

        # Confirm the bearer token equals the defined secret
        return parts[1] == self.secret

    def main(self) -> bool:
        # Run any required commands before we `git pull`
        if not self.run_commands(self.commands["before_pull"]):
            return False

        # Run any required commands after the `git pull`
        return self.run_commands(self.commands["after_pull"])
