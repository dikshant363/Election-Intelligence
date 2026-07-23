"""FastAPI dependency injection providers."""

from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.services import AIService
from app.application.handlers import CommandHandlers, QueryHandlers
from app.application.pipeline import CommandPipeline
from app.database.session import AsyncSessionLocal, get_db_session
from app.observability.services import ObservabilityService
from app.performance.services import PerformanceService
from app.persistence.uow import SqlAlchemyUnitOfWork, UnitOfWork
from app.production.services import ProductionService
from app.realtime.services import RealtimeService
from app.search.services import SearchService


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


def get_search_service(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> SearchService:
    """Provide SearchService instance via SAL."""
    return SearchService(session=session)


def get_ai_service(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> AIService:
    """Provide AIService instance."""
    return AIService(session=session)


def get_realtime_service() -> RealtimeService:
    """Provide global RealtimeService instance."""
    return RealtimeService()


def get_observability_service(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> ObservabilityService:
    """Provide ObservabilityService instance."""
    return ObservabilityService(session=session)


def get_performance_service() -> PerformanceService:
    """Provide global PerformanceService instance."""
    return PerformanceService()


def get_production_service() -> ProductionService:
    """Provide global ProductionService instance."""
    return ProductionService()
