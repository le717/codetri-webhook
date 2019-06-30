from importlib import import_module

from flask import current_app, Blueprint, request, Response

bp = Blueprint("root", __name__, url_prefix="")


def main() -> str:
    # Get the current endpoint and request data
    hook_request = request.get_json()
    this_endpoint = request.path.lstrip("/")

    # Get the config for this webhook
    # We don't have to check if this exists because we can only
    # acccess this endpoint because it's been defined
    hook_config = [
        hook
        for hook in current_app.config["SUPPORTED_HOOKS"]
        if hook["name"] == this_endpoint
    ][0]

    # Next, we import the defined service and give it the info it needs
    service = getattr(
        import_module(f"src.core.services.{hook_config['service']}"),
        hook_config["service"]
    )(**hook_config)
    service.headers = dict(request.headers)

    # Remove the request URL scheme and the trailing slash, if needed,
    # and add it to the service headers
    # TOD What about subdomains, e.g., `api.example.com`?
    url = request.url_root.replace(f"{request.scheme}://", "")
    if url.endswith("/"):
        url = url.rstrip("/")
    service.headers["Request-Url"] = url

    # Kick off the service process
    success = service.main()

    # Respond with the proper response code
    code = 200 if success else 400
    return Response("", code)
