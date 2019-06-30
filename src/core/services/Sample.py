from dataclasses import dataclass
from os.path import abspath, expanduser

from src.core.services.base import Base


@dataclass
class Sample(Base):
    def main(self) -> bool:
        # Check if this is an authorized request
        if not self.is_authorized("SAMPLE_TOKEN"):
            return False

        # Run any required commands before we `git pull`
        if self.before_pull:
            before_result = self.run_commands(self.before_pull)
        if not before_result:
            return False

        # Run any required commands after the `git pull`
        if self.after_pull:
            after_result = self.run_commands(self.after_pull)
        if not after_result:
            return False

        # Everything worked! Woo! :D
        return True
