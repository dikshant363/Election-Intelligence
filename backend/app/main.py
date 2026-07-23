"""Main application entrypoint."""

import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api import api_router
from app.api.v1.errors import register_error_handlers
from app.config import settings
from app.identity.exceptions import AuthenticationError, AuthorizationError
from app.identity.middleware import identity_context_middleware
from app.logging import configure_logging
from app.security import (
    RequestLimitMiddleware,
    SecurityHeadersMiddleware,
    request_id_middleware,
    setup_cors,
    setup_trusted_hosts,
)

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

    # Configure security and identity middlewares
    application.middleware("http")(identity_context_middleware)
    application.middleware("http")(request_id_middleware)
    application.add_middleware(SecurityHeadersMiddleware)
    application.add_middleware(RequestLimitMiddleware)
    setup_cors(application)
    setup_trusted_hosts(application)

    # Register RFC 7807 error handlers
    register_error_handlers(application)

    # Register identity exception handlers
    @application.exception_handler(AuthenticationError)
    async def authentication_exception_handler(
        request: Request, exc: AuthenticationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=401,
            content={
                "type": "https://api.electionintelligence.org/errors/unauthorized",
                "title": "Unauthorized",
                "status": 401,
                "detail": exc.message,
                "instance": request.url.path,
                "code": exc.code,
            },
        )

    @application.exception_handler(AuthorizationError)
    async def authorization_exception_handler(
        request: Request, exc: AuthorizationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=403,
            content={
                "type": "https://api.electionintelligence.org/errors/forbidden",
                "title": "Forbidden",
                "status": 403,
                "detail": exc.message,
                "instance": request.url.path,
                "code": exc.code,
            },
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
    """Application shutting down."""
    logger.info("Application shutting down")
