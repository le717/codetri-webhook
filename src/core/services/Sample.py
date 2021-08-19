from dataclasses import dataclass

from src.core.services.base import Base


@dataclass
class Sample(Base):
    def is_authorized(self) -> bool:
        """Check if this is an authorized request."""
        secret_key = self.headers["X-SAMPLE-TOKEN"]
        return secret_key == self.secret

    def main(self) -> bool:
        # Run any required commands before we `git pull`
        if self.before_pull:
            if not self.run_commands(self.before_pull):
                return False

        # Run any required commands after the `git pull`
        if self.after_pull:
            if not self.run_commands(self.after_pull):
                return False

        # Everything worked! Woo! :D
        return True
