"""Election Domain Value Objects."""

import re
import uuid
from dataclasses import dataclass
from datetime import date
from enum import StrEnum

from app.domain.common.base import Identifier, ValueObject

MIN_STATE_CODE_LEN = 2
MAX_STATE_CODE_LEN = 10
MIN_LATITUDE = -90.0
MAX_LATITUDE = 90.0
MIN_LONGITUDE = -180.0
MAX_LONGITUDE = 180.0
MAX_PERCENTAGE = 100.0
MAX_AGE_YEARS = 150
MIN_PHONE_DIGITS = 10
MAX_PHONE_DIGITS = 15


@dataclass(frozen=True)
class ElectionId(Identifier):
    """Unique identifier for an Election aggregate."""

    @classmethod
    def generate(cls) -> "ElectionId":
        """Generate a new ElectionId with UUIDv4."""
        return cls(value=uuid.uuid4())


@dataclass(frozen=True)
class CandidateId(Identifier):
    """Unique identifier for a Candidate aggregate."""

    @classmethod
    def generate(cls) -> "CandidateId":
        """Generate a new CandidateId with UUIDv4."""
        return cls(value=uuid.uuid4())


@dataclass(frozen=True)
class PartyId(Identifier):
    """Unique identifier for a PoliticalParty aggregate."""

    @classmethod
    def generate(cls) -> "PartyId":
        """Generate a new PartyId with UUIDv4."""
        return cls(value=uuid.uuid4())


@dataclass(frozen=True)
class ConstituencyId(Identifier):
    """Unique identifier for a Constituency aggregate."""

    @classmethod
    def generate(cls) -> "ConstituencyId":
        """Generate a new ConstituencyId with UUIDv4."""
        return cls(value=uuid.uuid4())


@dataclass(frozen=True)
class PollingBoothId(Identifier):
    """Unique identifier for a PollingBooth aggregate."""

    @classmethod
    def generate(cls) -> "PollingBoothId":
        """Generate a new PollingBoothId with UUIDv4."""
        return cls(value=uuid.uuid4())


class ElectionType(StrEnum):
    """Types of elections held."""

    GENERAL = "GENERAL"
    ASSEMBLY = "ASSEMBLY"
    BYE_ELECTION = "BYE_ELECTION"
    MUNICIPAL = "MUNICIPAL"
    LOCAL_BODY = "LOCAL_BODY"


@dataclass(frozen=True)
class StateCode(ValueObject):
    """State or Union Territory code (e.g. IN-DL, IN-MH)."""

    code: str

    def __post_init__(self) -> None:
        if (
            not self.code
            or len(self.code) < MIN_STATE_CODE_LEN
            or len(self.code) > MAX_STATE_CODE_LEN
        ):
            raise ValueError(f"Invalid StateCode: {self.code}")


@dataclass(frozen=True)
class DistrictCode(ValueObject):
    """District code within a state."""

    code: str

    def __post_init__(self) -> None:
        if not self.code or not self.code.strip():
            raise ValueError("DistrictCode cannot be empty.")


@dataclass(frozen=True)
class AssemblyCode(ValueObject):
    """Legislative Assembly constituency code."""

    code: str

    def __post_init__(self) -> None:
        if not self.code or not self.code.strip():
            raise ValueError("AssemblyCode cannot be empty.")


@dataclass(frozen=True)
class ParliamentCode(ValueObject):
    """Parliamentary constituency code."""

    code: str

    def __post_init__(self) -> None:
        if not self.code or not self.code.strip():
            raise ValueError("ParliamentCode cannot be empty.")


@dataclass(frozen=True)
class GeoCoordinates(ValueObject):
    """WGS84 geographic coordinates (latitude and longitude)."""

    latitude: float
    longitude: float

    def __post_init__(self) -> None:
        if not (MIN_LATITUDE <= self.latitude <= MAX_LATITUDE):
            raise ValueError(f"Latitude out of range [-90, 90]: {self.latitude}")
        if not (MIN_LONGITUDE <= self.longitude <= MAX_LONGITUDE):
            raise ValueError(
                f"Longitude out of range [-180, 180]: {self.longitude}"
            )


@dataclass(frozen=True)
class ElectionDate(ValueObject):
    """Election scheduling date range."""

    start_date: date
    end_date: date

    def __post_init__(self) -> None:
        if self.end_date < self.start_date:
            raise ValueError("end_date cannot be earlier than start_date.")


@dataclass(frozen=True)
class VoteCount(ValueObject):
    """Non-negative vote tally count."""

    count: int

    def __post_init__(self) -> None:
        if self.count < 0:
            raise ValueError(f"VoteCount cannot be negative: {self.count}")

    def add(self, other: "VoteCount") -> "VoteCount":
        """Combine two vote counts."""
        return VoteCount(count=self.count + other.count)


@dataclass(frozen=True)
class Percentage(ValueObject):
    """Validated vote percentage between 0.0 and 100.0."""

    value: float

    def __post_init__(self) -> None:
        if not (0.0 <= self.value <= MAX_PERCENTAGE):
            raise ValueError(
                f"Percentage must be between 0.0 and 100.0: {self.value}"
            )


@dataclass(frozen=True)
class Age(ValueObject):
    """Candidate age in years."""

    years: int

    def __post_init__(self) -> None:
        if self.years < 0 or self.years > MAX_AGE_YEARS:
            raise ValueError(f"Invalid age: {self.years}")


@dataclass(frozen=True)
class Email(ValueObject):
    """Validated email address."""

    address: str

    def __post_init__(self) -> None:
        regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(regex, self.address):
            raise ValueError(f"Invalid email address format: {self.address}")


@dataclass(frozen=True)
class PhoneNumber(ValueObject):
    """Validated contact phone number."""

    number: str

    def __post_init__(self) -> None:
        digits = re.sub(r"\D", "", self.number)
        if len(digits) < MIN_PHONE_DIGITS or len(digits) > MAX_PHONE_DIGITS:
            raise ValueError(f"Invalid phone number format: {self.number}")
