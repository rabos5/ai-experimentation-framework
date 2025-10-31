import os
from collections import OrderedDict
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from app.config import (
    APP_INFO,
    FASTAPI_ENV,
    FASTAPI_LOGGER_NAME,
    FASTAPI_LOG_LEVEL,
    POETRY_LOCK
)
from app.core.exceptions import ApiException
from app.core.logger import get_logger


logger = get_logger(FASTAPI_LOGGER_NAME, FASTAPI_LOG_LEVEL)
api_router = APIRouter()


@api_router.get("/health", tags=["server"])
@api_router.get("/status", tags=["server"])
def get_server_status() -> JSONResponse:
    content = {
        "status": "healthy"
    }

    return JSONResponse(
        status_code=200,
        content=content
    )


@api_router.get("/info", tags=["server"])
def get_server_info() -> JSONResponse:
    try:
        status_code = 200
        success = True
        data = None
        error = None

        data = {
            "app": APP_INFO
        }

        if FASTAPI_ENV.lower() in ["local", "dev", "dit"]:
            data["env"] = dict(OrderedDict(sorted(os.environ.items())))
            packages = POETRY_LOCK.get("package", [])
            data["dependencies"] = { i["name"]: i["version"] for i in packages }
    except Exception as e:
        logger.error(f"Internal server error -> {str(e)}", exc_info=True)
        raise ApiException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            success=False,
            data=None,
            error="Internal server error"
        )

    content = {
        "success": success,
        "data": data,
        "error": error
    }

    return JSONResponse(
        status_code=status_code,
        content=content
    )