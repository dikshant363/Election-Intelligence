"""Application handlers package initialization."""

from app.application.handlers.command_handlers import CommandHandlers
from app.application.handlers.query_handlers import QueryHandlers

__all__ = ["CommandHandlers", "QueryHandlers"]
