import gzip
import json
import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import Message
from typing import Callable, List
from app.config import (
    FASTAPI_LOGGER_NAME,
    FASTAPI_LOG_LEVEL
)
from app.core.logger import get_logger


logger = get_logger(FASTAPI_LOGGER_NAME, FASTAPI_LOG_LEVEL)
HEADERS_TO_FORWARD = []


class HeaderMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        headers_to_forward: List[str] = HEADERS_TO_FORWARD
    ):
        super().__init__(app)
        self.headers_to_forward = headers_to_forward

    async def dispatch(self, request: Request, call_next: Callable):
        response = await call_next(request)

        for header in self.headers_to_forward:
            if header_value := request.headers.get(header):
                response.headers[header] = header_value

        return response
    

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        start_time = time.time()
        await self._log_request(request)
        response = await call_next(request)
        response_body = await self._get_response_body(response)
        end_time = time.time()
        total_time = end_time - start_time
        response.headers["X-Process-Time"] = f"{total_time:.4f}s"
        await self._log_response(request, response, response_body, total_time)
       
        return response
   
    async def _log_request(self, request: Request):
        log_dict = {
            "type": "request",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "method": request.method,
            "path": request.url.path,
            "query_params": str(request.query_params),
            "client": request.client.host if request.client else None
        }
       
        if FASTAPI_LOG_LEVEL == "debug":
            body = await self._get_request_body(request)
            log_dict.update({
                "headers": dict(request.headers),
                "body": body
            })

        logger.info(json.dumps(log_dict, indent=2))

    async def _log_response(self, request: Request, response: Response, response_body: str, process_time: float):
        log_dict = {
            "type": "response",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "path": request.url.path,
            "status_code": response.status_code,
            "process_time": f"{process_time:.4f}s"
        }
       
        if FASTAPI_LOG_LEVEL == "debug":
            log_dict.update({
                "headers": dict(response.headers),
                "body": response_body
            })

        logger.info(json.dumps(log_dict, indent=2))

    async def _get_request_body(self, request: Request) -> str:
        if request.method.upper() not in {"POST", "PUT", "PATCH", "DELETE", "OPTIONS"}:
            return ""

        content_length = request.headers.get("content-length")
        if content_length is not None and int(content_length) == 0:
            return ""

        body = await request.body()

        async def receive() -> Message:
            return {"type": "http.request", "body": body, "more_body": False}
        request._receive = receive
       
        try:
            return body.decode("utf-8")
        except UnicodeDecodeError:
            return "<binary>"

    async def _get_response_body(self, response: Response) -> str:
        try:
            body = b""
            async for chunk in response.body_iterator:
                body += chunk
           
            async def new_iterator():
                yield body
            response.body_iterator = new_iterator()

            if response.headers.get("content-encoding") == "gzip":
                try:
                    body = gzip.decompress(body)
                    response.headers["content-length"] = str(len(body))
                    del response.headers["content-encoding"]
                except Exception as e:
                    logger.error(f"Error decompressing gzip response body -> {e}")
                    return "<error decompressing gzip response body>"
           
            try:
                return body.decode("utf-8")
            except UnicodeDecodeError:
                return "<binary>"
        except Exception as e:
            logger.error(f"Error getting response body: {e}")
            return "<error reading response body>"