from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from app.config import (
    APP_DESCRIPTION,
    APP_NAME,
    APP_VERSION,
    FASTAPI_ENV,
    FASTAPI_LOGGER_NAME,
    FASTAPI_LOG_LEVEL
)
from app.core.exceptions import add_exception_handlers
from app.core.logger import get_logger
from app.core.middleware import HeaderMiddleware, LoggingMiddleware
from app.routes import server, api, ui


logger = get_logger(FASTAPI_LOGGER_NAME, FASTAPI_LOG_LEVEL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("starting up...")
    # add startup tasks here
    logger.info("startup successful...")
    yield
    logger.info("shutting down...")
    # add shutdown tasks here
    pass

app = FastAPI(
    lifespan=lifespan
)

app.mount("/assets", StaticFiles(directory="assets"), name="assets")
app.mount("/css", StaticFiles(directory="css"), name="css")
app.mount("/js", StaticFiles(directory="js"), name="js")
# not needed to mount html files as we read them from within the routes; this way not all html files are accessible by default
# app.mount("/static", StaticFiles(directory="static"), name="static")

# api docs
def openapi_config():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=APP_NAME,
        version=APP_VERSION,
        description=APP_DESCRIPTION,
        routes=app.routes
    )

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = openapi_config

# add exception handlers
add_exception_handlers(app)

# add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],
    allow_credentials=True,
    allow_methods=[
        # "DELETE",
        "OPTIONS",
        "GET",
        "POST"
    ],
    allow_headers=[
        "*"
    ]
)

app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(HeaderMiddleware)
if FASTAPI_ENV.lower() not in ["prod", "production"]:
    app.add_middleware(LoggingMiddleware)

# include api routes / routers
app.include_router(
    server.api_router,
    tags=["server"],
    dependencies=[]
)

app.include_router(
    api.api_router,
    tags=["api"],
    dependencies=[]
)

app.include_router(
    ui.api_router,
    tags=["ui"],
    dependencies=[]
)