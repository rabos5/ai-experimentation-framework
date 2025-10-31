from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from typing import Optional
from app.config import FASTAPI_LOGGER_NAME, FASTAPI_LOG_LEVEL
from app.core.logger import get_logger

logger = get_logger(FASTAPI_LOGGER_NAME, FASTAPI_LOG_LEVEL)


# Simple exception class (idiomatic Python for exceptions)
class ApiException(Exception):
    def __init__(self, status_code: int, error: str = "", success: bool = False, data=None):
        super().__init__(error)
        self.status_code = status_code
        self.error = error
        self.success = success
        self.data = data


def create_error_response(status_code: int, error_message: str, headers: Optional[dict] = None):
    """Create a standardized error JSON response."""
    content = {
        "success": False,
        "data": None,
        "error": error_message
    }
    response = JSONResponse(status_code=status_code, content=content)
    if headers:
        for key, value in headers.items():
            response.headers[key] = value
    return response


def add_exception_handlers(app: FastAPI):
    """Register exception handlers for the FastAPI app."""
    
    # Custom API exception handler
    async def api_exception_handler(request: Request, exc: ApiException):
        return create_error_response(exc.status_code, exc.error)
    
    app.exception_handler(ApiException)(api_exception_handler)
    
    # Define standard HTTP error handlers configuration
    error_handlers_config = {
        400: {
            "message": "Bad request - invalid or malformed request",
            "headers": None,
            "log_error": False,
        },
        401: {
            "message": "Unauthorized - authentication required",
            "headers": {"WWW-Authenticate": "Bearer"},
            "log_error": False,
        },
        403: {
            "message": "Forbidden - insufficient permissions",
            "headers": None,
            "log_error": False,
        },
        500: {
            "message": "Internal server error",
            "headers": None,
            "log_error": True,
        },
    }
    
    def create_status_handler(status_code: int, config: dict):
        """Factory function to create HTTP status code handlers."""
        async def handler(request: Request, exc):
            if config["log_error"]:
                logger.error(
                    f"{config['message']} -> {request.method} {request.url.path}",
                    exc_info=True
                )
            return create_error_response(
                status_code,
                config["message"],
                config.get("headers")
            )
        return handler
    
    for status_code, config in error_handlers_config.items():
        app.exception_handler(status_code)(
            create_status_handler(status_code, config)
        )