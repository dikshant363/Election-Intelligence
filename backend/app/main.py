"""Main application entrypoint."""

import logging

from fastapi import FastAPI

from app.api import api_router
from app.config import settings
from app.logging import configure_logging

configure_logging()
logger = logging.getLogger(__name__)


def create_application() -> FastAPI:
    """Application factory."""
    application = FastAPI(
        title=settings.PROJECT_NAME,
        description="Election Intelligence Platform API",
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url=f"{settings.API_V1_STR}/docs",
        redoc_url=f"{settings.API_V1_STR}/redoc",
    )

    application.include_router(api_router, prefix=settings.API_V1_STR)

    return application


app = create_application()


@app.on_event("startup")
async def startup_event() -> None:
    """Application startup."""
    logger.info("Application starting up")


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Application shutdown."""
    logger.info("Application shutting down")
