from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from app.config import (
    FASTAPI_LOGGER_NAME,
    FASTAPI_LOG_LEVEL
)
from app.core.exceptions import ApiException
from app.core.logger import get_logger


logger = get_logger(FASTAPI_LOGGER_NAME, FASTAPI_LOG_LEVEL)
api_router = APIRouter()


# todo: declare api routes
@api_router.get("/sample", tags=["api"])
def get_server_info() -> JSONResponse:
    try:
        status_code = 200
        success = True
        data = None
        error = None

        data = {}
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