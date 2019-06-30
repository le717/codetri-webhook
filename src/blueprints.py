from flask import Blueprint


def _factory(partial_module_string: str, url_prefix: str) -> Blueprint:
    import_name = f"src.views.{partial_module_string}"
    blueprint = Blueprint(
        partial_module_string,
        import_name,
        url_prefix=url_prefix
    )
    return blueprint


def _route():
    pass

root = _factory("root", "/")

all_blueprints = (root,)
