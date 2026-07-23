"""Unit tests for election domain aggregates and invariants."""

from datetime import date

import pytest
from app.domain.candidate import Candidate
from app.domain.constituency import Constituency
from app.domain.election import Election, ElectionStatus
from app.domain.party import PoliticalParty
from app.domain.polling import PollingBooth
from app.domain.results import ElectionResult
from app.domain.value_objects import (
    Age,
    CandidateId,
    ConstituencyId,
    ElectionDate,
    ElectionId,
    ElectionType,
    Email,
    GeoCoordinates,
    PartyId,
    PhoneNumber,
    PollingBoothId,
    StateCode,
    VoteCount,
)


def test_election_aggregate_lifecycle() -> None:
    """Verify Election status transitions and event recording."""
    e_id = ElectionId.generate()
    election = Election(
        id=e_id,
        title="Lok Sabha General Election",
        election_type=ElectionType.GENERAL,
        election_date=ElectionDate(
            start_date=date(2026, 4, 1), end_date=date(2026, 5, 1)
        ),
    )

    assert election.status == ElectionStatus.DRAFT
    assert len(election.domain_events) == 1

    # Start election
    election.start_election()
    assert election.status == ElectionStatus.ACTIVE

    # Complete election
    election.complete_election()
    assert election.status == ElectionStatus.COMPLETED

    # Cannot cancel completed election
    with pytest.raises(ValueError, match="Cannot cancel a completed election"):
        election.cancel_election()


def test_candidate_aggregate_party_assignment() -> None:
    """Verify Candidate aggregate creation and party assignment."""
    c_id = CandidateId.generate()
    con_id = ConstituencyId.generate()
    p_id = PartyId.generate()

    candidate = Candidate(
        id=c_id,
        name="Aarav Sharma",
        age=Age(35),
        email=Email("aarav@example.com"),
        phone=PhoneNumber("+919876543210"),
        constituency_id=con_id,
    )

    assert candidate.party_id is None
    assert len(candidate.domain_events) == 1

    candidate.assign_party(p_id)
    assert candidate.party_id == p_id


def test_political_party_aggregate_symbol_update() -> None:
    """Verify PoliticalParty aggregate and symbol updates."""
    p_id = PartyId.generate()
    party = PoliticalParty(
        id=p_id,
        name="National Progress Party",
        code="NPP",
        symbol="Lotus Flag",
    )

    assert party.symbol == "Lotus Flag"
    assert len(party.domain_events) == 1

    party.update_symbol("Rising Sun")
    assert party.symbol == "Rising Sun"


def test_constituency_and_polling_booth_aggregates() -> None:
    """Verify Constituency and PollingBooth aggregate initializations."""
    con_id = ConstituencyId.generate()
    constituency = Constituency(
        id=con_id,
        name="New Delhi",
        code="DL-01",
        state_code=StateCode("IN-DL"),
    )
    assert constituency.name == "New Delhi"

    booth_id = PollingBoothId.generate()
    booth = PollingBooth(
        id=booth_id,
        constituency_id=con_id,
        booth_name="Central School Booth 1",
        booth_number="PB-101",
        location=GeoCoordinates(latitude=28.6139, longitude=77.2090),
    )
    assert booth.booth_name == "Central School Booth 1"
    assert len(booth.domain_events) == 1


def test_election_result_aggregate_vote_recording_and_declaration() -> None:
    """Verify ElectionResult vote tallies and declaration lifecycle."""
    e_id = ElectionId.generate()
    con_id = ConstituencyId.generate()
    c1 = CandidateId.generate()
    c2 = CandidateId.generate()

    res = ElectionResult(election_id=e_id, constituency_id=con_id)
    assert res.is_declared is False

    res.record_votes(c1, VoteCount(5000))
    res.record_votes(c2, VoteCount(4500))

    assert res.total_votes.count == 9500

    res.declare_result(winning_candidate_id=c1)
    assert res.is_declared is True
    assert res.winning_candidate_id == c1
    assert len(res.domain_events) == 1

    # Cannot modify votes after declaration
    with pytest.raises(ValueError, match="Cannot modify vote tallies"):
        res.record_votes(c1, VoteCount(6000))
