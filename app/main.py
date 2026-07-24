"""Election Intelligence Platform - FastAPI Application Entry Point."""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
)
logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    app_name: str = "Election Intelligence Platform"
    app_version: str = "0.1.0"
    debug: bool = False
    database_url: str = ""
    redis_url: str = ""
    secret_key: str = ""
    cors_origins: str = "*"

    model_config = {"env_file": ".env"}


settings = Settings()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins.split(",") if settings.cors_origins != "*" else ["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

    # Include routers
    from app.api.health import router as health_router
    from app.api.version import router as version_router

    app.include_router(health_router)
    app.include_router(version_router)

    return app


app = create_app()


@app.get("/")
async def root():
    """Root endpoint returning basic platform information."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "operational",
        "docs": "/docs"
    }


logger.info(f"Starting {settings.app_name} v{settings.app_version}")
