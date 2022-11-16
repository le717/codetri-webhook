import hashlib
import hmac
from json import dumps, loads

from werkzeug.urls import url_decode

from src.core.logger import LOG


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
            raise TypeError(
                "Request body type must be set, either JSON or form parameter."
            )

        # Parse the request body as desired
        if self.body and self.is_json:
            self.body = loads(self.body.decode())
            return None
        if self.body and self.is_form:
            self.body = url_decode(self.body)
            return None

    def is_authorized(self) -> bool:
        # https://docs.github.com/en/developers/webhooks-and-events/webhooks/webhook-events-and-payloads#delivery-headers
        # Make sure this user-agent is from from GitHub
        is_github = self.headers["User-Agent"].startswith("GitHub-Hookshot/")
        if not is_github:
            LOG.error("This request's User-Agent is not from github.com!")
            LOG.info(f"User-Agent provided: {self.headers['User-Agent']}")

        # Make sure we have the signature
        if (expected := self.headers.get("X-Hub-Signature-256")) is None:
            LOG.error("X-Hub-Signature-256 header was not provided!")
            return False

        # Calculate the payload signature to ensure it's correct
        # https://developer.github.com/webhooks/securing/
        msg = dumps(self.body, separators=(",", ":")).encode("utf-8")
        signature = hmac.new(
            self.secret.encode("utf-8"), msg=msg, digestmod=hashlib.sha256
        ).hexdigest()
        digests_are_equal = hmac.compare_digest(signature, expected[7:])

        if not digests_are_equal:
            LOG.error("Payload signatures do not match!")
        return is_github and digests_are_equal