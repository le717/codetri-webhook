from importlib import import_module

from flask import Blueprint, current_app, request


bp = Blueprint("root", __name__, url_prefix="")


def main() -> tuple[dict, int]:
    # Get the current endpoint and request data
    this_endpoint = request.path.lstrip("/")

    # Get the config for this webhook
    # We don't have to check if this exists since
    # we are only here because it's been defined
    hook = current_app.config["SUPPORTED_HOOKS"][this_endpoint]

    # Next, we import the defined service and give it the info it needs
    service = getattr(import_module(f"services.{hook['service']}"), hook["service"])(
        **hook,
        headers=request.headers,
        body=request.data,
    )

    # The service didn't receive proper auth
    if not service.is_authorized():
        return {"status": "Incorrect authentication credentials."}, 403

    # Run the service's entrypoint and respond appropriately
    if service.main():
        return {}, 200
    return {"status": "Error running webhook service."}, 400
