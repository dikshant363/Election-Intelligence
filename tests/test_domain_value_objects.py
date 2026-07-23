"""Unit tests for election domain value objects."""

from datetime import date

import pytest

from app.domain.value_objects import (
    Age,
    CandidateId,
    ConstituencyId,
    ElectionDate,
    ElectionId,
    Email,
    GeoCoordinates,
    PartyId,
    Percentage,
    PhoneNumber,
    PollingBoothId,
    StateCode,
    VoteCount,
)


def test_identifiers_generation() -> None:
    """Verify identifier value object generation."""
    e_id = ElectionId.generate()
    c_id = CandidateId.generate()
    p_id = PartyId.generate()
    con_id = ConstituencyId.generate()
    b_id = PollingBoothId.generate()

    assert str(e_id) is not None
    assert str(c_id) is not None
    assert str(p_id) is not None
    assert str(con_id) is not None
    assert str(b_id) is not None


def test_state_code_validation() -> None:
    """Verify StateCode validation rules."""
    valid_state = StateCode("IN-DL")
    assert valid_state.code == "IN-DL"

    with pytest.raises(ValueError, match="Invalid StateCode"):
        StateCode("X")


def test_geo_coordinates_validation() -> None:
    """Verify GeoCoordinates latitude/longitude boundaries."""
    coords = GeoCoordinates(latitude=28.6139, longitude=77.2090)
    assert coords.latitude == 28.6139
    assert coords.longitude == 77.2090

    with pytest.raises(ValueError, match="Latitude out of range"):
        GeoCoordinates(latitude=95.0, longitude=77.0)

    with pytest.raises(ValueError, match="Longitude out of range"):
        GeoCoordinates(latitude=28.0, longitude=190.0)


def test_election_date_validation() -> None:
    """Verify ElectionDate start and end date rules."""
    valid_date = ElectionDate(
        start_date=date(2026, 5, 1),
        end_date=date(2026, 5, 10),
    )
    assert valid_date.start_date < valid_date.end_date

    with pytest.raises(ValueError, match="end_date cannot be earlier"):
        ElectionDate(
            start_date=date(2026, 5, 10),
            end_date=date(2026, 5, 1),
        )


def test_vote_count_addition_and_validation() -> None:
    """Verify VoteCount addition and non-negative constraint."""
    v1 = VoteCount(100)
    v2 = VoteCount(50)
    v3 = v1.add(v2)
    assert v3.count == 150

    with pytest.raises(ValueError, match="VoteCount cannot be negative"):
        VoteCount(-1)


def test_percentage_validation() -> None:
    """Verify Percentage range constraints."""
    p = Percentage(45.5)
    assert p.value == 45.5

    with pytest.raises(ValueError, match="Percentage must be between"):
        Percentage(105.0)


def test_age_email_phone_validation() -> None:
    """Verify Age, Email, and PhoneNumber validation rules."""
    age = Age(30)
    assert age.years == 30

    with pytest.raises(ValueError, match="Invalid age"):
        Age(-5)

    email = Email("candidate@election.org")
    assert email.address == "candidate@election.org"

    with pytest.raises(ValueError, match="Invalid email address format"):
        Email("invalid-email")

    phone = PhoneNumber("+919876543210")
    assert phone.number == "+919876543210"

    with pytest.raises(ValueError, match="Invalid phone number format"):
        PhoneNumber("123")
