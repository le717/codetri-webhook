import hashlib
import hmac
from json import loads
from urllib.parse import parse_qs

from src.core.logger import logger


__all__ = ["GitHubAuthMixin"]


class GitHubAuthMixin:
    """Service mixin to authorize GitHub webhook requests.

    Do not use this class directly! Create a class that inherits from
    `GitHubAuthMixin, BaseMixin` to create a Service.
    """

    is_json: bool = False
    is_form: bool = False

    def preprocess(self) -> None:
        # One of the options must be set
        if not self.is_json and not self.is_form:
            raise TypeError("Request body type must be set, either JSON or form parameter.")

        # Parse the request body as desired
        if self.body and self.is_json:
            self.body = loads(self.raw_body.decode())
            return None
        if self.body and self.is_form:
            self.body = parse_qs(self.raw_body)
            return None

    def is_authorized(self) -> bool:
        # https://docs.github.com/en/developers/webhooks-and-events/webhooks/webhook-events-and-payloads#delivery-headers
        # Make sure this user-agent is from from GitHub
        if not self.headers["User-Agent"].startswith("GitHub-Hookshot/"):
            logger.error(
                "This request's User-Agent is not from github.com! "
                f"User-Agent provided: {self.headers['User-Agent']}"
            )
            return False

        # Make sure we have the signature
        if (expected := self.headers.get("X-Hub-Signature-256")) is None:
            logger.error("X-Hub-Signature-256 header was not provided!")
            return False

        # Calculate the payload signature to ensure it's correct
        # https://developer.github.com/webhooks/securing/
        signature = hmac.new(
            self.secret.encode(), msg=self.raw_body, digestmod=hashlib.sha256
        ).hexdigest()

        # The payload signatures match, we're good
        if hmac.compare_digest(signature, expected[7:]):
            return True

        logger.error("Payload signatures do not match!")
        return False
