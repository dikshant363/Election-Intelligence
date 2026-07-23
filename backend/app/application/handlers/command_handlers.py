"""CQRS Command Handlers orchestrating domain aggregates, repositories, and UoW."""

import uuid

from app.application.commands import (
    CreateConstituency,
    CreateElection,
    CreatePollingBooth,
    DeclareResult,
    RegisterCandidate,
    RegisterParty,
)
from app.application.dto import (
    CandidateDTO,
    ConstituencyDTO,
    ElectionDTO,
    ElectionResultDTO,
    PartyDTO,
    PollingBoothDTO,
)
from app.application.events import EventDispatcher
from app.core.events import EventBus
from app.core.result import DomainError, ErrorCode, Result
from app.domain.candidate import Candidate
from app.domain.constituency import Constituency
from app.domain.election import Election
from app.domain.party import PoliticalParty
from app.domain.polling import PollingBooth
from app.domain.results import ElectionResult
from app.domain.specifications import CandidateEligibility
from app.domain.value_objects import (
    Age,
    CandidateId,
    ConstituencyId,
    ElectionDate,
    ElectionId,
    Email,
    GeoCoordinates,
    PartyId,
    PhoneNumber,
    PollingBoothId,
    StateCode,
    VoteCount,
)
from app.persistence.uow import UnitOfWork


class CommandHandlers:
    """Application Command Handlers coordinating business workflows."""

    def __init__(
        self,
        uow: UnitOfWork,
        event_bus: EventBus | None = None,
    ) -> None:
        self._uow = uow
        self._dispatcher = EventDispatcher(event_bus=event_bus)

    async def handle_create_election(
        self, command: CreateElection
    ) -> Result[ElectionDTO]:
        """Handle CreateElection command."""
        try:
            e_id = ElectionId.generate()
            election = Election(
                id=e_id,
                title=command.title,
                election_type=command.election_type,
                election_date=ElectionDate(
                    start_date=command.start_date,
                    end_date=command.end_date,
                ),
            )
            async with self._uow:
                await self._uow.elections.add(election)
                await self._uow.commit()

            await self._dispatcher.dispatch_events_for(election)
            return Result.ok(ElectionDTO.from_domain(election))
        except ValueError as val_err:
            return Result.fail(
                DomainError(
                    message=str(val_err),
                    code=ErrorCode.VALIDATION_ERROR,
                )
            )
        except Exception as err:
            return Result.fail(
                DomainError(
                    message=f"Failed to create election: {err}",
                    code=ErrorCode.INTERNAL_ERROR,
                )
            )

    async def handle_register_party(
        self, command: RegisterParty
    ) -> Result[PartyDTO]:
        """Handle RegisterParty command."""
        try:
            p_id = PartyId.generate()
            party = PoliticalParty(
                id=p_id,
                name=command.name,
                code=command.code,
                symbol=command.symbol,
            )
            async with self._uow:
                existing = await self._uow.parties.find_by_code(command.code)
                if existing:
                    return Result.fail(
                        DomainError(
                            message=f"Party with code '{command.code}' already exists.",
                            code=ErrorCode.CONFLICT,
                        )
                    )
                await self._uow.parties.add(party)
                await self._uow.commit()

            await self._dispatcher.dispatch_events_for(party)
            return Result.ok(PartyDTO.from_domain(party))
        except ValueError as val_err:
            return Result.fail(
                DomainError(
                    message=str(val_err),
                    code=ErrorCode.VALIDATION_ERROR,
                )
            )

    async def handle_create_constituency(
        self, command: CreateConstituency
    ) -> Result[ConstituencyDTO]:
        """Handle CreateConstituency command."""
        try:
            con_id = ConstituencyId.generate()
            constituency = Constituency(
                id=con_id,
                name=command.name,
                code=command.code,
                state_code=StateCode(code=command.state_code),
                constituency_type=command.constituency_type,
            )
            async with self._uow:
                existing = await self._uow.constituencies.find_by_code(
                    command.code
                )
                if existing:
                    return Result.fail(
                        DomainError(
                            message=f"Constituency code '{command.code}' already exists.",
                            code=ErrorCode.CONFLICT,
                        )
                    )
                await self._uow.constituencies.add(constituency)
                await self._uow.commit()

            return Result.ok(ConstituencyDTO.from_domain(constituency))
        except ValueError as val_err:
            return Result.fail(
                DomainError(
                    message=str(val_err),
                    code=ErrorCode.VALIDATION_ERROR,
                )
            )

    async def handle_register_candidate(
        self, command: RegisterCandidate
    ) -> Result[CandidateDTO]:
        """Handle RegisterCandidate command."""
        try:
            cand_id = CandidateId.generate()
            con_id = ConstituencyId(value=uuid.UUID(command.constituency_id))
            party_id = (
                PartyId(value=uuid.UUID(command.party_id))
                if command.party_id
                else None
            )

            candidate = Candidate(
                id=cand_id,
                name=command.name,
                age=Age(years=command.age),
                email=Email(address=command.email),
                phone=PhoneNumber(number=command.phone),
                constituency_id=con_id,
                party_id=party_id,
            )

            # Enforce candidate eligibility specification
            eligibility_spec = CandidateEligibility()
            if not eligibility_spec.is_satisfied_by(candidate):
                return Result.fail(
                    DomainError(
                        message=f"Candidate age ({command.age}) does not meet eligibility criteria.",
                        code=ErrorCode.VALIDATION_ERROR,
                    )
                )

            async with self._uow:
                # Verify constituency exists
                constituency = await self._uow.constituencies.get_by_id(con_id)
                if not constituency:
                    return Result.fail(
                        DomainError(
                            message=f"Constituency '{command.constituency_id}' not found.",
                            code=ErrorCode.NOT_FOUND,
                        )
                    )

                await self._uow.candidates.add(candidate)
                await self._uow.commit()

            await self._dispatcher.dispatch_events_for(candidate)
            return Result.ok(CandidateDTO.from_domain(candidate))
        except ValueError as val_err:
            return Result.fail(
                DomainError(
                    message=str(val_err),
                    code=ErrorCode.VALIDATION_ERROR,
                )
            )

    async def handle_create_polling_booth(
        self, command: CreatePollingBooth
    ) -> Result[PollingBoothDTO]:
        """Handle CreatePollingBooth command."""
        try:
            booth_id = PollingBoothId.generate()
            con_id = ConstituencyId(value=uuid.UUID(command.constituency_id))

            booth = PollingBooth(
                id=booth_id,
                constituency_id=con_id,
                booth_name=command.booth_name,
                booth_number=command.booth_number,
                location=GeoCoordinates(
                    latitude=command.latitude,
                    longitude=command.longitude,
                ),
            )

            async with self._uow:
                constituency = await self._uow.constituencies.get_by_id(con_id)
                if not constituency:
                    return Result.fail(
                        DomainError(
                            message=f"Constituency '{command.constituency_id}' not found.",
                            code=ErrorCode.NOT_FOUND,
                        )
                    )

                await self._uow.polling_booths.add(booth)
                await self._uow.commit()

            await self._dispatcher.dispatch_events_for(booth)
            return Result.ok(PollingBoothDTO.from_domain(booth))
        except ValueError as val_err:
            return Result.fail(
                DomainError(
                    message=str(val_err),
                    code=ErrorCode.VALIDATION_ERROR,
                )
            )

    async def handle_declare_result(
        self, command: DeclareResult
    ) -> Result[ElectionResultDTO]:
        """Handle DeclareResult command."""
        try:
            e_id = ElectionId(value=uuid.UUID(command.election_id))
            con_id = ConstituencyId(value=uuid.UUID(command.constituency_id))
            winner_id = (
                CandidateId(value=uuid.UUID(command.winning_candidate_id))
                if command.winning_candidate_id
                else None
            )

            async with self._uow:
                election = await self._uow.elections.get_by_id(e_id)
                if not election:
                    return Result.fail(
                        DomainError(
                            message=f"Election '{command.election_id}' not found.",
                            code=ErrorCode.NOT_FOUND,
                        )
                    )

                constituency = await self._uow.constituencies.get_by_id(con_id)
                if not constituency:
                    return Result.fail(
                        DomainError(
                            message=f"Constituency '{command.constituency_id}' not found.",
                            code=ErrorCode.NOT_FOUND,
                        )
                    )

                # Rehydrate or create ElectionResult
                result = await self._uow.results.find_by_election_and_constituency(
                    e_id, con_id
                )
                if not result:
                    result = ElectionResult(
                        election_id=e_id, constituency_id=con_id
                    )

                for c_id_str, count in command.candidate_votes.items():
                    c_id = CandidateId(value=uuid.UUID(c_id_str))
                    result.record_votes(c_id, VoteCount(count=count))

                result.declare_result(winning_candidate_id=winner_id)

                if await self._uow.results.exists(str(result.id)):
                    await self._uow.results.update(result)
                else:
                    await self._uow.results.add(result)

                await self._uow.commit()

            await self._dispatcher.dispatch_events_for(result)
            return Result.ok(ElectionResultDTO.from_domain(result))
        except ValueError as val_err:
            return Result.fail(
                DomainError(
                    message=str(val_err),
                    code=ErrorCode.VALIDATION_ERROR,
                )
            )
