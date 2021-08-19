from importlib import import_module

from flask import current_app, Blueprint, request, Response

bp = Blueprint("root", __name__, url_prefix="")


def main() -> str:
    # Get the current endpoint and request data
    this_endpoint = request.path.lstrip("/")

    # Get the config for this webhook
    # We don't have to check if this exists since
    # we are only here because it's been defined
    hook_config = current_app.config["SUPPORTED_HOOKS"][this_endpoint]

    # Next, we import the defined service and give it the info it needs
    service = getattr(
        import_module(f"src.core.services.{hook_config['service']}"),
        hook_config["service"],
    )(**hook_config)
    service.headers = dict(request.headers)
    service.body = request.get_json()

    # Kick off the service if authorized
    success = False
    if service.is_authorized():
        success = service.main()

    # Respond with the proper response code
    code = 200 if success else 400
    return Response("", code)
