"""API router registering health check endpoints and v1 domain routers."""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from app.api.v1.dependencies.dependencies import get_observability_service
from app.api.v1.routers.ai import router as ai_router
from app.api.v1.routers.candidates import router as candidates_router
from app.api.v1.routers.constituencies import router as constituencies_router
from app.api.v1.routers.elections import router as elections_router
from app.api.v1.routers.observability import router as observability_router
from app.api.v1.routers.parties import router as parties_router
from app.api.v1.routers.performance import router as performance_router
from app.api.v1.routers.polling_booths import router as polling_router
from app.api.v1.routers.production import router as production_router
from app.api.v1.routers.realtime import router as realtime_router
from app.api.v1.routers.results import router as results_router
from app.api.v1.routers.search import router as search_router
from app.config import settings
from app.logging import get_logger
from app.observability.schemas import HealthResponseSchema
from app.observability.services import ObservabilityService

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


@api_router.get(
    "/health",
    response_model=HealthResponseSchema,
    tags=["Observability & Operations"],
    summary="Get overall platform health and component dependencies status",
)
async def health_endpoint(
    obs_service: ObservabilityService = Depends(get_observability_service),
) -> HealthResponseSchema:
    """Health check endpoint with database and dependency status."""
    return await obs_service.get_readiness()


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
api_router.include_router(search_router)
api_router.include_router(ai_router)
api_router.include_router(realtime_router)
api_router.include_router(observability_router)
api_router.include_router(performance_router)
api_router.include_router(production_router)
