from importlib import import_module

from flask import Flask
from flask import abort
from werkzeug.contrib.fixers import ProxyFix

from src.core.app_config import load_app_config, load_hook_configs
from src.views import root


def create_app():
    app = Flask(__name__)
    # https://stackoverflow.com/a/45333882
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.config.update(load_app_config())

    # Load the supported hooks
    app.config["SUPPORTED_HOOKS"] = []
    for hook in load_hook_configs():
        app.config["SUPPORTED_HOOKS"].append(hook)

        # Create an endpoint for each hook
        root.bp.add_url_rule(
            f"/{hook['name']}".lower(),
            hook["name"],
            root.main,
            methods=["POST"]
        )

    # Register the blueprint
    app.register_blueprint(root.bp)

    # All access to undefined routes are bad requests
    @app.errorhandler(404)
    def not_found_handler(e):
        abort(400)

    return app



