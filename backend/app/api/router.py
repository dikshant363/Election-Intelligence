"""API router."""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database.session import get_db_session
from app.logging import get_logger

logger = get_logger(__name__)

api_router = APIRouter()


@api_router.get("/", tags=["health"])
async def root_endpoint(request: Request) -> JSONResponse:
    """Root endpoint (version 1)."""
    return JSONResponse(
        {
            "message": "Election Intelligence Platform API",
            "version": settings.VERSION,
            "status": "operational",
        }
    )


@api_router.get("/health", tags=["health"])
async def health_endpoint(
    request: Request,
    db: AsyncSession = Depends(get_db_session),
) -> JSONResponse:
    """Health check endpoint with database connectivity test."""
    logger.info("Health check requested")
    db_status = "disconnected"
    try:
        result = await db.execute(text("SELECT 1"))
        if result.scalar() == 1:
            db_status = "connected"
    except Exception as exc:
        logger.error(f"Database connectivity check failed: {exc}")
        db_status = "disconnected"

    status = "healthy" if db_status == "connected" else "degraded"
    return JSONResponse(
        {
            "status": status,
            "database": db_status,
        }
    )


@api_router.get("/version", tags=["health"])
async def version_endpoint(request: Request) -> JSONResponse:
    """Version information endpoint."""
    logger.info("Version requested")
    return JSONResponse(
        {
            "version": settings.VERSION,
            "api_version": "v1",
        }
    )
