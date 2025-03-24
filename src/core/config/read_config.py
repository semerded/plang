import os
from ...typedef import path
from ... import data
from shutil import copyfile
import json

config_file_path_possibilities: list[path] = ["", "config", "src", "src/config", ]

def find_config_file(path) -> path:
    for path in config_file_path_possibilities:
        config_file_path = os.path.join(data.cwd, path, ".plang")
        if os.path.isfile(config_file_path):
            return config_file_path
        
    # no config file found
    config_file_path = os.path.join(data.cwd, ".plang")
    copyfile(os.path.join(data.lib_path, "core", "config", "default_config.json"), config_file_path)
    return config_file_path

def read_config_file(path) -> None:
    with open(path, "r") as f:
        config = json.load(f)
        
    data.debugging = config.get("debug", False)
        
    messenger_config = config.get("messenger", {})
    
    data.add_console_timestamp = messenger_config.get("add_console_timestamp", True)
    
    logger_config = config.get("logger", {})
        
    data.log_file_location = os.path.join(data.cwd, logger_config.get("log_file_location", "log"))
    data.logging_enabled = logger_config.get("logging_enabled", True)
    data.log_file_limit = logger_config.get("log_file_limit", 100)
    