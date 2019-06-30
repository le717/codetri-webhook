from json import load
from os import listdir
from os.path import join

from dotenv import dotenv_values, find_dotenv


__all__ = [
    "load_app_config",
    "load_hook_configs"
]


def load_app_config() -> dict:
    """Load the env variables from file."""
    vals = {}
    env_vals = dotenv_values(find_dotenv())
    for key, value in env_vals.items():
        vals[key] = (value if value != "" else None)
    return vals


def load_hook_configs():
    # Find out what hooks have been defined
    HOOKS_PATH = "hooks"
    hooks = []
    available_hooks = listdir(HOOKS_PATH)

    # Load the available hooks
    for hook_file in available_hooks:
        with open(join(HOOKS_PATH, hook_file), "rt") as f:
            yield load(f)
