"""Version endpoint for Election Intelligence Platform."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/version")
async def get_version():
    """Return the current version of the application."""
    return {
        "name": "Election Intelligence Platform",
        "version": "0.1.0",
        "api_version": "v1",
        "build_date": "2024-01-15",
        "commit": "initial-release",
        "python_version": "3.12.0",
        "platform": "linux"
    }