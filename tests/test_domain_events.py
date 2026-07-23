"""Unit tests for election domain events."""

from app.domain.candidate import CandidateRegistered
from app.domain.election import ElectionCreated
from app.domain.party import PartyRegistered
from app.domain.polling import PollingBoothCreated
from app.domain.results import ResultDeclared
from app.domain.value_objects import (
    CandidateId,
    ConstituencyId,
    ElectionId,
    ElectionType,
    PartyId,
    PollingBoothId,
    VoteCount,
)


def test_domain_events_instantiation() -> None:
    """Verify domain events data structure and occurred_at timestamps."""
    e_id = ElectionId.generate()
    c_id = CandidateId.generate()
    p_id = PartyId.generate()
    con_id = ConstituencyId.generate()
    b_id = PollingBoothId.generate()

    e_created = ElectionCreated(
        election_id=e_id,
        title="Lok Sabha 2026",
        election_type=ElectionType.GENERAL,
    )
    assert e_created.election_id == e_id
    assert e_created.occurred_at is not None

    c_registered = CandidateRegistered(
        candidate_id=c_id,
        name="Candidate Name",
        constituency_id=con_id,
        party_id=p_id,
    )
    assert c_registered.candidate_id == c_id

    p_registered = PartyRegistered(
        party_id=p_id,
        name="Party Name",
        code="PN",
    )
    assert p_registered.party_id == p_id

    b_created = PollingBoothCreated(
        booth_id=b_id,
        constituency_id=con_id,
        booth_number="PB-01",
    )
    assert b_created.booth_id == b_id

    r_declared = ResultDeclared(
        election_id=e_id,
        constituency_id=con_id,
        winning_candidate_id=c_id,
        total_votes=VoteCount(10000),
    )
    assert r_declared.winning_candidate_id == c_id
    assert r_declared.total_votes.count == 10000
