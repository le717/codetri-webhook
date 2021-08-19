import logging
import sys

from flask import Flask, Response
from werkzeug.middleware.proxy_fix import ProxyFix

from src.core import config
from src.views import root


def create_app():
    # Create a logger
    logger = logging.getLogger("codetri-webhook")
    logger.setLevel(logging.INFO)
    LOG_MSG_FORMAT = logging.Formatter("[%(asctime)s - %(levelname)s]: %(message)s")
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(LOG_MSG_FORMAT)
    logger.addHandler(handler)

    # Create the app
    app = Flask(__name__)
    # https://stackoverflow.com/a/45333882
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.config.update(config.app())

    # Load the supported hooks
    app.config["SUPPORTED_HOOKS"] = {}
    for hook in config.hooks():
        app.config["SUPPORTED_HOOKS"].update({hook["name"]: hook})

        # Create an endpoint for each hook
        root.bp.add_url_rule(
            f"/{hook['name']}".lower(), hook["name"], root.main, methods=["POST"]
        )

    # Register the blueprint
    app.register_blueprint(root.bp)

    # All access to undefined routes are bad requests
    @app.errorhandler(404)
    def not_found_handler(e) -> Response:
        return Response("", 400)

    return app
