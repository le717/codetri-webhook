from re import match
from typing import Optional, Tuple, Union


__all__ = ["get_git_branch_or_tag", "make_response", "make_error_response"]


def get_git_branch_or_tag(ref: str) -> Union[str, None]:
    regex = r"refs/(?:tags|heads)/([\w\d._-]+)"
    matches = match(regex, ref)
    if matches:
        return matches.group(1)
    return None


def make_response(status: int, data: Optional[str] = None) -> Tuple[str, int]:
    """Construct a non-error endpoint response."""
    if data is None:
        data = ""
    return (data, status)


def make_error_response(status: int, msg: str) -> Tuple[str, int]:
    """Construct an error endpoint response."""
    return make_response(status, msg)
