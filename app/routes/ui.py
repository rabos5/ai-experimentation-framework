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


@api_router.get("/sample_page_tailwind_css")
async def get_sample_page_tailwind_css(request: Request) -> HTMLResponse:
    with open(os.path.join(get_base_dir(), "static", "sample_page_tailwind_css.html"), "r") as f:
        html_template = f.read()
        template = Template(html_template)
        rendered_html = template.render()

    return HTMLResponse(
        status_code=200,
        content=rendered_html
    )


@api_router.get("/ai_experimentation_framework")
async def get_ai_experimentation_framework(request: Request) -> HTMLResponse:
    with open(os.path.join(get_base_dir(), "static", "ai_experimentation_framework.html"), "r") as f:
        html_template = f.read()
        template = Template(html_template)
        rendered_html = template.render()

    return HTMLResponse(
        status_code=200,
        content=rendered_html
    )