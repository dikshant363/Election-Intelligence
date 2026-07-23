"""API v1 dependencies package initialization."""

from app.api.v1.dependencies.dependencies import (
    get_command_handlers,
    get_command_pipeline,
    get_query_handlers,
    get_uow,
)

__all__ = [
    "get_command_handlers",
    "get_command_pipeline",
    "get_query_handlers",
    "get_uow",
]
