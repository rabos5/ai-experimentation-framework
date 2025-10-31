import json
import logging.config
import os
from functools import lru_cache
from app.core.utils import get_base_dir


VALID_LOG_LEVELS = [
    "info",
    "debug",
    "error",
    "warning",
    "fail"
]

@lru_cache(maxsize=1)
def get_logger(logger_name: str, log_level: str):
    log_level = log_level.lower()
    if log_level not in VALID_LOG_LEVELS:
        raise ValueError(f"Invalid 'log_level' -> '{log_level}'. Must be one of {VALID_LOG_LEVELS}")
    
    logging_config_path = os.path.join(get_base_dir(), "app", "core", "logging.config")
    with open(logging_config_path, "r") as logging_config_file:
        logging_config = json.load(logging_config_file)

    updated_loggers = {}
    for key, value in logging_config.get("loggers", {}).items():
        new_key = key.replace("logger_name_", f"{logger_name}_")
        updated_loggers[new_key] = value
    
    logging_config["loggers"] = updated_loggers
    logging.config.dictConfig(logging_config)

    return logging.getLogger(f"{logger_name}_{log_level}")