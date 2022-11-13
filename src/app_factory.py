from os import getenv

from flask import Flask, Response
from werkzeug.middleware.proxy_fix import ProxyFix

from src.core import config, logger
from src.views import root


def create_app():
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(
        app.wsgi_app,
        x_for=1,
        x_proto=1,
        x_host=1,
        x_prefix=1,
    )

    # Load the app configuration
    app.config.update(config.app("default"))
    app.config.update(config.app(getenv("FLASK_ENV")))

    # Create an app error log and general runtime logs
    app.logger.addHandler(logger.file_handler("error.log"))
    logger.LOG.addHandler(logger.file_handler("general.log"))

    # Load the hooks
    app.config["SUPPORTED_HOOKS"] = {}
    for hook in config.hooks():
        # Don't load the Sample hook in production
        if getenv("FLASK_ENV") == "production" and hook["name"] == "sample":
            continue

        # Create an endpoint for each hook
        app.config["SUPPORTED_HOOKS"].update({hook["name"]: hook})
        root.bp.add_url_rule(
            f"/{hook['name']}".lower(),
            hook["name"],
            root.main,
            methods=["POST"],
        )

    # Register the blueprint
    app.register_blueprint(root.bp)

    @app.errorhandler(404)
    def not_found_handler(e) -> Response:
        """All access to undefined routes are bad requests."""
        return {}, 400

    @app.errorhandler(405)
    def method_not_allowed_handler(e) -> Response:
        """Only POST requests are allowed."""
        return {}, 400

    return app
