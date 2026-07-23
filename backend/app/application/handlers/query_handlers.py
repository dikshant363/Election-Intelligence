"""CQRS Query Handlers providing read-only DTO projections."""

import uuid

from app.application.dto import (
    CandidateDTO,
    ConstituencyDTO,
    ElectionDTO,
    ElectionResultDTO,
    PartyDTO,
)
from app.application.queries import (
    GetCandidate,
    GetConstituency,
    GetElection,
    GetParty,
    GetResult,
    ListCandidates,
    ListConstituencies,
    ListElections,
    ListParties,
)
from app.core.result import DomainError, ErrorCode, Result
from app.domain.election import ElectionStatus
from app.domain.value_objects import (
    CandidateId,
    ConstituencyId,
    ElectionId,
    PartyId,
)
from app.persistence.uow import UnitOfWork


class QueryHandlers:
    """Application Query Handlers producing read-only DTO views."""

    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def handle_get_election(
        self, query: GetElection
    ) -> Result[ElectionDTO]:
        """Handle GetElection query."""
        try:
            e_id = ElectionId(value=uuid.UUID(query.id))
            async with self._uow:
                election = await self._uow.elections.get_by_id(e_id)
                if not election:
                    return Result.fail(
                        DomainError(
                            message=f"Election '{query.id}' not found.",
                            code=ErrorCode.NOT_FOUND,
                        )
                    )
                return Result.ok(ElectionDTO.from_domain(election))
        except ValueError:
            return Result.fail(
                DomainError(
                    message=f"Invalid election ID format: '{query.id}'",
                    code=ErrorCode.VALIDATION_ERROR,
                )
            )

    async def handle_list_elections(
        self, query: ListElections
    ) -> Result[list[ElectionDTO]]:
        """Handle ListElections query."""
        async with self._uow:
            if query.status:
                status_enum = ElectionStatus(query.status)
                elections = await self._uow.elections.find_by_status(status_enum)
            else:
                elections = await self._uow.elections.find_all(
                    skip=query.skip, limit=query.limit
                )
            dtos = [ElectionDTO.from_domain(e) for e in elections]
            return Result.ok(dtos)

    async def handle_get_candidate(
        self, query: GetCandidate
    ) -> Result[CandidateDTO]:
        """Handle GetCandidate query."""
        try:
            c_id = CandidateId(value=uuid.UUID(query.id))
            async with self._uow:
                candidate = await self._uow.candidates.get_by_id(c_id)
                if not candidate:
                    return Result.fail(
                        DomainError(
                            message=f"Candidate '{query.id}' not found.",
                            code=ErrorCode.NOT_FOUND,
                        )
                    )
                return Result.ok(CandidateDTO.from_domain(candidate))
        except ValueError:
            return Result.fail(
                DomainError(
                    message=f"Invalid candidate ID format: '{query.id}'",
                    code=ErrorCode.VALIDATION_ERROR,
                )
            )

    async def handle_list_candidates(
        self, query: ListCandidates
    ) -> Result[list[CandidateDTO]]:
        """Handle ListCandidates query."""
        async with self._uow:
            if query.constituency_id:
                con_id = ConstituencyId(value=uuid.UUID(query.constituency_id))
                candidates = await self._uow.candidates.find_by_constituency(
                    con_id
                )
            elif query.party_id:
                p_id = PartyId(value=uuid.UUID(query.party_id))
                candidates = await self._uow.candidates.find_by_party(p_id)
            else:
                candidates = await self._uow.candidates.find_all(
                    skip=query.skip, limit=query.limit
                )
            dtos = [CandidateDTO.from_domain(c) for c in candidates]
            return Result.ok(dtos)

    async def handle_get_party(self, query: GetParty) -> Result[PartyDTO]:
        """Handle GetParty query."""
        async with self._uow:
            party = None
            if query.id:
                p_id = PartyId(value=uuid.UUID(query.id))
                party = await self._uow.parties.get_by_id(p_id)
            elif query.code:
                party = await self._uow.parties.find_by_code(query.code)

            if not party:
                return Result.fail(
                    DomainError(
                        message="Party not found.",
                        code=ErrorCode.NOT_FOUND,
                    )
                )
            return Result.ok(PartyDTO.from_domain(party))

    async def handle_list_parties(
        self, query: ListParties
    ) -> Result[list[PartyDTO]]:
        """Handle ListParties query."""
        async with self._uow:
            parties = await self._uow.parties.find_all(
                skip=query.skip, limit=query.limit
            )
            dtos = [PartyDTO.from_domain(p) for p in parties]
            return Result.ok(dtos)

    async def handle_get_constituency(
        self, query: GetConstituency
    ) -> Result[ConstituencyDTO]:
        """Handle GetConstituency query."""
        async with self._uow:
            constituency = None
            if query.id:
                c_id = ConstituencyId(value=uuid.UUID(query.id))
                constituency = await self._uow.constituencies.get_by_id(c_id)
            elif query.code:
                constituency = await self._uow.constituencies.find_by_code(
                    query.code
                )

            if not constituency:
                return Result.fail(
                    DomainError(
                        message="Constituency not found.",
                        code=ErrorCode.NOT_FOUND,
                    )
                )
            return Result.ok(ConstituencyDTO.from_domain(constituency))

    async def handle_list_constituencies(
        self, query: ListConstituencies
    ) -> Result[list[ConstituencyDTO]]:
        """Handle ListConstituencies query."""
        async with self._uow:
            if query.state_code:
                constituencies = await self._uow.constituencies.find_by_state(
                    query.state_code
                )
            else:
                constituencies = await self._uow.constituencies.find_all(
                    skip=query.skip, limit=query.limit
                )
            dtos = [ConstituencyDTO.from_domain(c) for c in constituencies]
            return Result.ok(dtos)


    async def handle_get_result(
        self, query: GetResult
    ) -> Result[ElectionResultDTO]:
        """Handle GetResult query."""
        try:
            e_id = ElectionId(value=uuid.UUID(query.election_id))
            con_id = ConstituencyId(value=uuid.UUID(query.constituency_id))
            async with self._uow:
                res = await self._uow.results.find_by_election_and_constituency(
                    e_id, con_id
                )
                if not res:
                    return Result.fail(
                        DomainError(
                            message=f"Election result for election '{query.election_id}' and constituency '{query.constituency_id}' not found.",
                            code=ErrorCode.NOT_FOUND,
                        )
                    )
                return Result.ok(ElectionResultDTO.from_domain(res))
        except ValueError:
            return Result.fail(
                DomainError(
                    message="Invalid ID format provided in GetResult query.",
                    code=ErrorCode.VALIDATION_ERROR,
                )
            )
