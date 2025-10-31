import uvicorn
from app.config import (
    FASTAPI_HOST,
    FASTAPI_PORT,
    FASTAPI_WORKERS,
    FASTAPI_LOGGER_NAME,
    FASTAPI_LOG_LEVEL
)
from app.core.logger import get_logger
from app.core.utils import get_ssl_files


if __name__ == "__main__":
    proto = "http"
    logger = get_logger(FASTAPI_LOGGER_NAME, FASTAPI_LOG_LEVEL)
    debug = FASTAPI_LOG_LEVEL.lower() == "debug"

    uvicorn_config = {
        "app": "app.main:app",
        "host": FASTAPI_HOST,
        "port": FASTAPI_PORT,
        "workers": FASTAPI_WORKERS,
        "access_log": False,
        "reload": debug,
        "log_level": FASTAPI_LOG_LEVEL
    }

    ssl_keyfile, ssl_certfile = get_ssl_files()
    if ssl_keyfile and ssl_certfile:
        proto = "https"
        uvicorn_config.update(
            {
                "ssl_keyfile": ssl_keyfile,
                "ssl_certfile": ssl_certfile
            }
        )

    logger.info(f"starting server on {proto}://{FASTAPI_HOST}:{FASTAPI_PORT} {"in 'debug' mode" if debug else ""}")
    uvicorn.run(**uvicorn_config)