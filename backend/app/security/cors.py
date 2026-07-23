"""CORS security configuration."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings


def setup_cors(app: FastAPI) -> None:
    """Configure CORS middleware on the FastAPI application."""
    origins = list(settings.ALLOWED_ORIGINS)

    if settings.ENVIRONMENT == "production" and "*" in origins:
        origins = [origin for origin in origins if origin != "*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID"],
    )
