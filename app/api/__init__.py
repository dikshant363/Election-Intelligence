"""API package for Election Intelligence Platform."""

from fastapi import APIRouter
from app.api.health import health_check
from app.api.version import router as version_router

# Create main router
router = APIRouter()

# Include health check endpoint
router.add_api_route("/health", health_check, methods=["GET"])
router.include_router(version_router)