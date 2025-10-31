import os
import uuid
from cerberus import Validator
from datetime import datetime
from dotenv import load_dotenv
from functools import lru_cache
from typing import Any, Tuple


def format_timestamp(t = None, f = "%Y-%m-%dT%H:%M:%S.%f%z") -> str:
    if t in [None, ""]:
        return None

    t = datetime.strptime(t, f)
    return datetime.strftime(t, "%Y-%m-%dT%H:%M:%S")


def generate_id():
    return str(uuid.uuid4())


@lru_cache(maxsize=1)
def get_base_dir():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")


def get_ssl_files(*, key_file: str = "ssl.key", cert_file: str = "ssl.cert") -> Tuple[str, str]:
    key = os.getenv("FASTAPI_SSL_KEY", key_file)
    cert = os.getenv("FASTAPI_SSL_CERT", cert_file)

    def validate_file_exists(file_path: str) -> str:
        return file_path if os.path.isfile(file_path) else ""
    
    def validate_file_location(file_name: str) -> str:
        if os.path.dirname(file_name):
            return validate_file_exists(file_name)
        
        certs_path = os.path.join(get_base_dir(), "certs", file_name)
        return validate_file_exists(certs_path)
    
    return validate_file_location(key), validate_file_location(cert)


def load_env(*, base_dir: str, env: str) -> None:
    env_file = os.path.join(base_dir, f".env.{env}")

    if os.path.exists(env_file):
        load_dotenv(env_file)
    else:
        load_dotenv()

    return None


def validate_config(config: dict[str, Any]) -> None:
    missing_config = []
    for key, value in config.items():
        if not key.startswith("__"):
            if value in [None]:
                missing_config.append(key)

    if missing_config:
        raise ValueError(
            f"the following required config variables are not assigned: ",
            f"{', '.join(missing_config)}"
        )
    
    return None


def validate_input(input: dict, schema: dict):
    v = Validator(schema)
    if not v.validate(input):
        raise InputValidationError(v.errors)
    
    return v.document


class InputValidationError(Exception):
    pass