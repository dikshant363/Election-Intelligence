"""API v1 routers package initialization."""

from fastapi import APIRouter

from app.api.v1.routers.ai import router as ai_router
from app.api.v1.routers.candidates import router as candidates_router
from app.api.v1.routers.constituencies import router as constituencies_router
from app.api.v1.routers.elections import router as elections_router
from app.api.v1.routers.parties import router as parties_router
from app.api.v1.routers.polling_booths import router as polling_router
from app.api.v1.routers.results import router as results_router
from app.api.v1.routers.search import router as search_router

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(elections_router)
api_v1_router.include_router(candidates_router)
api_v1_router.include_router(parties_router)
api_v1_router.include_router(constituencies_router)
api_v1_router.include_router(polling_router)
api_v1_router.include_router(results_router)
api_v1_router.include_router(search_router)
api_v1_router.include_router(ai_router)

__all__ = [
    "api_v1_router",
    "candidates_router",
    "constituencies_router",
    "elections_router",
    "parties_router",
    "polling_router",
    "results_router",
    "search_router",
    "ai_router",
]
