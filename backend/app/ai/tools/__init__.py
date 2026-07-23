"""AI Tools interfacing exclusively with Application Layer QueryHandlers & Search Platform SAL."""

from __future__ import annotations

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.application.handlers import QueryHandlers
from app.application.queries import GetCandidate, GetConstituency, GetElection
from app.persistence.uow import SqlAlchemyUnitOfWork
from app.search.queries import SearchQuery
from app.search.services import SearchService


class AIToolkit:
    """
    AI Tools provider.
    Enables LLMs and RAG agents to query election data strictly through Application & Search Layer services.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._search_service = SearchService(session)
        # Create UoW and QueryHandlers for Application Layer access
        self._uow = SqlAlchemyUnitOfWork(lambda: session)
        self._query_handlers = QueryHandlers(uow=self._uow)

    async def search_tool(self, query: str) -> dict[str, Any]:
        """Execute full-text search across election platform."""
        res = await self._search_service.search(SearchQuery(raw_query=query))
        return {
            "total": res.total,
            "hits": [
                {
                    "id": h.id,
                    "type": h.entity_type,
                    "title": h.title,
                    "snippet": h.highlight,
                }
                for h in res.hits
            ],
        }

    async def election_lookup_tool(self, election_id: str) -> dict[str, Any]:
        """Lookup election details via Application Layer QueryHandlers."""
        res = await self._query_handlers.handle_get_election(GetElection(id=election_id))
        if res.is_failure:
            return {"error": res.error.message}
        dto = res.unwrap()
        return {
            "id": str(dto.id),
            "title": dto.title,
            "election_type": dto.election_type,
            "status": dto.status,
            "start_date": str(dto.start_date),
            "end_date": str(dto.end_date),
        }

    async def candidate_lookup_tool(self, candidate_id: str) -> dict[str, Any]:
        """Lookup candidate details via Application Layer QueryHandlers."""
        res = await self._query_handlers.handle_get_candidate(GetCandidate(id=candidate_id))
        if res.is_failure:
            return {"error": res.error.message}
        dto = res.unwrap()
        return {
            "id": str(dto.id),
            "name": dto.name,
            "party_id": str(dto.party_id) if dto.party_id else None,
            "constituency_id": str(dto.constituency_id),
            "age": dto.age,
        }

    async def constituency_lookup_tool(self, constituency_id: str) -> dict[str, Any]:
        """Lookup constituency details via Application Layer QueryHandlers."""
        res = await self._query_handlers.handle_get_constituency(
            GetConstituency(id=constituency_id)
        )
        if res.is_failure:
            return {"error": res.error.message}
        dto = res.unwrap()
        return {
            "id": str(dto.id),
            "name": dto.name,
            "code": dto.code,
            "state_code": dto.state_code,
            "constituency_type": dto.constituency_type,
        }

    async def analytics_tool(self) -> dict[str, Any]:
        """Fetch statistical aggregations via Search Layer Analytics."""
        by_state = await self._search_service.get_analytics_by_state()
        by_party = await self._search_service.get_analytics_by_party()
        turnout = await self._search_service.get_turnout_statistics()
        return {
            "constituencies_by_state": by_state.data,
            "candidates_by_party": by_party.data,
            "turnout_stats": turnout,
        }
