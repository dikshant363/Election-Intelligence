"""Unit of Work interface and SqlAlchemy implementation."""

from abc import ABC, abstractmethod
from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.domain.candidate import CandidateRepository
from app.domain.constituency import ConstituencyRepository
from app.domain.election import ElectionRepository
from app.domain.party import PartyRepository
from app.domain.polling import PollingBoothRepository
from app.domain.results import ResultRepository
from app.persistence.repositories import (
    SqlAlchemyCandidateRepository,
    SqlAlchemyConstituencyRepository,
    SqlAlchemyElectionRepository,
    SqlAlchemyPartyRepository,
    SqlAlchemyPollingRepository,
    SqlAlchemyResultRepository,
)


class UnitOfWork(ABC):
    """Abstract Unit of Work contract establishing transaction boundaries."""

    elections: ElectionRepository
    candidates: CandidateRepository
    parties: PartyRepository
    constituencies: ConstituencyRepository
    polling_booths: PollingBoothRepository
    results: ResultRepository

    async def __aenter__(self) -> "UnitOfWork":
        """Enter transaction context manager."""
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit transaction context manager with automatic rollback on exception."""
        if exc_type is not None:
            await self.rollback()

    @abstractmethod
    async def commit(self) -> None:
        """Commit transaction changes to database."""
        pass

    @abstractmethod
    async def rollback(self) -> None:
        """Rollback current transaction changes."""
        pass


class SqlAlchemyUnitOfWork(UnitOfWork):
    """SQLAlchemy 2.x async implementation of Unit of Work pattern."""

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession] | None = None,
        session: AsyncSession | None = None,
    ) -> None:
        self._session_factory = session_factory
        self._provided_session = session
        self._session: AsyncSession | None = session
        self._owns_session = False

    async def __aenter__(self) -> "SqlAlchemyUnitOfWork":
        if self._provided_session is not None:
            self._session = self._provided_session
            self._owns_session = False
        elif self._session_factory is not None:
            self._session = self._session_factory()
            self._owns_session = True
        else:
            raise ValueError("SqlAlchemyUnitOfWork requires session or session_factory.")

        self.elections = SqlAlchemyElectionRepository(self._session)
        self.candidates = SqlAlchemyCandidateRepository(self._session)
        self.parties = SqlAlchemyPartyRepository(self._session)
        self.constituencies = SqlAlchemyConstituencyRepository(self._session)
        self.polling_booths = SqlAlchemyPollingRepository(self._session)
        self.results = SqlAlchemyResultRepository(self._session)

        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        try:
            if exc_type is not None and self._session is not None:
                await self._session.rollback()
        finally:
            if self._owns_session and self._session is not None:
                await self._session.close()

    async def commit(self) -> None:
        if self._session is not None:
            await self._session.commit()

    async def rollback(self) -> None:
        if self._session is not None:
            await self._session.rollback()
