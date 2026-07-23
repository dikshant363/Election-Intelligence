"""Unit tests for domain specifications."""

from datetime import date

from app.domain.candidate import Candidate
from app.domain.constituency import Constituency
from app.domain.election import Election
from app.domain.party import PoliticalParty
from app.domain.specifications import (
    CandidateEligibility,
    ElectionOpen,
    UniquePartySymbol,
    ValidConstituency,
    ValidVotePercentage,
)
from app.domain.value_objects import (
    Age,
    CandidateId,
    ConstituencyId,
    ElectionDate,
    ElectionId,
    ElectionType,
    Email,
    PartyId,
    Percentage,
    PhoneNumber,
    StateCode,
)


def test_candidate_eligibility_specification() -> None:
    """Verify CandidateEligibility specification rules."""
    spec = CandidateEligibility(min_age_years=25)

    c_id = CandidateId.generate()
    con_id = ConstituencyId.generate()

    eligible_candidate = Candidate(
        id=c_id,
        name="Eligible Candidate",
        age=Age(28),
        email=Email("c1@example.com"),
        phone=PhoneNumber("+919876543210"),
        constituency_id=con_id,
    )
    ineligible_candidate = Candidate(
        id=CandidateId.generate(),
        name="Young Candidate",
        age=Age(21),
        email=Email("c2@example.com"),
        phone=PhoneNumber("+919876543210"),
        constituency_id=con_id,
    )

    assert spec.is_satisfied_by(eligible_candidate) is True
    assert spec.is_satisfied_by(ineligible_candidate) is False


def test_election_open_specification() -> None:
    """Verify ElectionOpen specification rules."""
    spec = ElectionOpen()

    election = Election(
        id=ElectionId.generate(),
        title="State Assembly Election",
        election_type=ElectionType.ASSEMBLY,
        election_date=ElectionDate(
            start_date=date(2026, 6, 1), end_date=date(2026, 6, 5)
        ),
    )

    assert spec.is_satisfied_by(election) is False
    election.start_election()
    assert spec.is_satisfied_by(election) is True


def test_valid_vote_percentage_and_party_specifications() -> None:
    """Verify Percentage, PartySymbol, and Constituency specifications."""
    perc_spec = ValidVotePercentage()
    assert perc_spec.is_satisfied_by(Percentage(45.0)) is True

    party_spec = UniquePartySymbol()
    party = PoliticalParty(
        id=PartyId.generate(),
        name="Reform Alliance",
        code="RA",
        symbol="Star",
    )
    assert party_spec.is_satisfied_by(party) is True

    con_spec = ValidConstituency()
    constituency = Constituency(
        id=ConstituencyId.generate(),
        name="South Mumbai",
        code="MH-24",
        state_code=StateCode("IN-MH"),
    )
    assert con_spec.is_satisfied_by(constituency) is True
