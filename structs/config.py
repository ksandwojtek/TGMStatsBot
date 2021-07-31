import json
from warnings import warn
from pathlib import Path
import os

from structs.global_vars import GlobalVariables


def get_config_file(config_path_string: str):
    config_location = Path(config_path_string).expanduser().resolve()

    try:
        # If the config location passed is the name of the config file in the current working directory
        # Or the full path, this will open it either way
        with open(config_location, mode="r") as config_file:
            config = json.loads(config_file.read())
        # If it's a directory we'll assume the file called config.json is the config
    except IsADirectoryError:
        with open(os.path.join(config_location, "config.json"), mode="r") as config_file:
            config = json.loads(config_file.read())
    except Exception as e:
        warn("Error finding and loading config file, using default config")
        return GlobalVariables().config
    return config


class Config:
    def __init__(self, config_location):
        # Argparse currently passes in arguments of certain types wrapped in a list when it shouldn't
        # This is workaround for that issue
        if isinstance(config_location, list):
            config_location = config_location[0]
        self.config = get_config_file(config_location)

    def get_config(self):
        return self.config
