from typing import Union
from re import match


__all__ = [
    "get_git_branch_or_tag"
]


def get_git_branch_or_tag(ref: str) -> Union[str, None]:
    regex = r"refs/(?:tags|heads)/([\w\d._-]+)"
    matches = match(regex, ref)
    if matches:
        return matches.group(1)
    return None
