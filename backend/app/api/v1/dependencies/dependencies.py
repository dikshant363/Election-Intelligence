"""FastAPI dependency injection providers."""

from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends

from app.application.handlers import CommandHandlers, QueryHandlers
from app.application.pipeline import CommandPipeline
from app.database.session import AsyncSessionLocal
from app.persistence.uow import SqlAlchemyUnitOfWork, UnitOfWork


async def get_uow() -> AsyncGenerator[UnitOfWork, None]:
    """Provide UnitOfWork dependency using AsyncSessionLocal factory."""
    uow = SqlAlchemyUnitOfWork(session_factory=AsyncSessionLocal)
    yield uow


def get_command_handlers(
    uow: Annotated[UnitOfWork, Depends(get_uow)],
) -> CommandHandlers:
    """Provide CommandHandlers instance."""
    return CommandHandlers(uow=uow)


def get_query_handlers(
    uow: Annotated[UnitOfWork, Depends(get_uow)],
) -> QueryHandlers:
    """Provide QueryHandlers instance."""
    return QueryHandlers(uow=uow)


def get_command_pipeline(
    handlers: Annotated[CommandHandlers, Depends(get_command_handlers)],
) -> CommandPipeline:
    """Provide CommandPipeline instance."""
    return CommandPipeline(handlers=handlers)
