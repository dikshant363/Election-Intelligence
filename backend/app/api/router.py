"""API router registering health check endpoints and v1 domain routers."""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.routers.candidates import router as candidates_router
from app.api.v1.routers.constituencies import router as constituencies_router
from app.api.v1.routers.elections import router as elections_router
from app.api.v1.routers.parties import router as parties_router
from app.api.v1.routers.polling_booths import router as polling_router
from app.api.v1.routers.results import router as results_router
from app.config import settings
from app.database.session import get_db_session
from app.logging import get_logger

logger = get_logger(__name__)

api_router = APIRouter()

# Register health check routes
@api_router.get("/", tags=["health"])
async def root_endpoint(request: Request) -> JSONResponse:
    """Root endpoint."""
    request_id = getattr(request.state, "request_id", "unknown")
    return JSONResponse(
        {
            "message": "Election Intelligence Platform API",
            "version": settings.VERSION,
            "status": "operational",
            "request_id": request_id,
        }
    )


@api_router.get("/health", tags=["health"])
async def health_endpoint(
    request: Request,
    db: AsyncSession = Depends(get_db_session),
) -> JSONResponse:
    """Health check endpoint with database connectivity status."""
    logger.info("Health check requested")
    db_status = "disconnected"
    try:
        result = await db.execute(text("SELECT 1"))
        if result.scalar() == 1:
            db_status = "connected"
    except Exception as exc:
        logger.error(f"Database connectivity check failed: {exc}")
        db_status = "disconnected"

    status_str = "healthy" if db_status == "connected" else "degraded"
    request_id = getattr(request.state, "request_id", "unknown")

    return JSONResponse(
        {
            "status": status_str,
            "database": db_status,
            "request_id": request_id,
        }
    )


@api_router.get("/version", tags=["health"])
async def version_endpoint(request: Request) -> JSONResponse:
    """Version information endpoint."""
    logger.info("Version requested")
    request_id = getattr(request.state, "request_id", "unknown")
    return JSONResponse(
        {
            "version": settings.VERSION,
            "api_version": "v1",
            "request_id": request_id,
        }
    )


# Register v1 domain entity routers
api_router.include_router(elections_router)
api_router.include_router(candidates_router)
api_router.include_router(parties_router)
api_router.include_router(constituencies_router)
api_router.include_router(polling_router)
api_router.include_router(results_router)
