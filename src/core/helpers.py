from typing import Optional, Tuple


__all__ = ["make_response", "make_error_response"]


def make_response(status: int, data: Optional[str] = None) -> Tuple[str, int]:
    """Construct a non-error endpoint response."""
    if data is None:
        data = ""
    return (data, status)


def make_error_response(status: int, msg: str) -> Tuple[str, int]:
    """Construct an error endpoint response."""
    return make_response(status, msg)
