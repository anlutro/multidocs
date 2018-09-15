import os
import os.path

from ._config import get_config


class Undefined:
    def __bool__(self):
        return False

    def __str__(self):
        return "UNDEFINED"

    def __repr__(self):
        return "<docgen.settings.Undefined>"


UNDEF = Undefined()


class Settings:
    def __init__(self, data):
        object.__setattr__(self, "_data", data)

    def __getattr__(self, key):
        return self._data.get(key, UNDEF)


def get_settings():
    # default values
    values = {}

    # config file
    config = get_config()
    if config and config.get("settings"):
        for key, val in config["settings"].items():
            values[key.lower()] = val

            # environment variables
    for key, val in os.environ.items():
        if not key.startswith("DOCGEN_"):
            continue
        key = key[7:].lower()
        values[key] = val

        # convertions
    for key, val in values.items():
        if key.endswith(("_dir", "_path")):
            values[key] = os.path.abspath(val)

    return Settings(values)
