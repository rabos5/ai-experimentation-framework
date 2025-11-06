import os
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from jinja2 import Template
from app.config import (
    FASTAPI_LOGGER_NAME,
    FASTAPI_LOG_LEVEL
)
from app.core.logger import get_logger
from app.core.utils import get_base_dir


logger = get_logger(FASTAPI_LOGGER_NAME, FASTAPI_LOG_LEVEL)
api_router = APIRouter()


@api_router.get("/sandbox")
async def get_sandbox(request: Request) -> HTMLResponse:
    with open(os.path.join(get_base_dir(), "static", "sandbox.html"), "r") as f:
        html_template = f.read()
        template = Template(html_template)
        rendered_html = template.render()

    return HTMLResponse(
        status_code=200,
        content=rendered_html
    )


@api_router.get("/chat")
async def get_chat(request: Request) -> HTMLResponse:
    with open(os.path.join(get_base_dir(), "static", "chat.html"), "r") as f:
        html_template = f.read()
        template = Template(html_template)
        rendered_html = template.render()

    return HTMLResponse(
        status_code=200,
        content=rendered_html
    )