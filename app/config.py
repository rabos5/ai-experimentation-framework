import os
import sys
import toml
from app.core.utils import load_env, get_base_dir, validate_config


# environment variable config
FASTAPI_ENV = os.getenv("FASTAPI_ENV", "local")
load_env(base_dir=get_base_dir(), env=FASTAPI_ENV)

# app / system config
PYPROJECT_TOML = toml.load(os.path.join(get_base_dir(), "pyproject.toml"))
POETRY_LOCK = toml.load(os.path.join(get_base_dir(), "poetry.lock"))
APP_NAME = PYPROJECT_TOML.get("project", {}).get("name", "")
APP_VERSION = PYPROJECT_TOML.get("project", {}).get("version", "")
APP_DESCRIPTION = PYPROJECT_TOML.get("project", {}).get("description", "")
APP_INFO = {
    "name": APP_NAME,
    "version": APP_VERSION,
    "description": APP_DESCRIPTION,
    "python_version": sys.version
}

# fastapi server config
FASTAPI_PROTO = os.getenv("FASTAPI_PROTO", "http").lower()
FASTAPI_HOST = "localhost" if FASTAPI_ENV.lower() == "local" else "0.0.0.0"
FASTAPI_PORT = int(os.getenv("FASTAPI_PORT", "5555"))
FASTAPI_WORKERS = int(os.getenv("FASTAPI_WORKERS", "1"))
FASTAPI_LOGGER_NAME = APP_NAME.replace("-", "_")
FASTAPI_LOG_LEVEL = os.getenv("FASTAPI_LOG_LEVEL", "debug").lower()

# fail application startup unless all constants above are assigned
validate_config(globals())