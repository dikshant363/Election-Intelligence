"""Election application command objects."""

from dataclasses import dataclass
from datetime import date

from app.domain.value_objects import ElectionType


@dataclass(frozen=True)
class CreateElection:
    """Command to schedule/create a new election."""

    title: str
    election_type: ElectionType
    start_date: date
    end_date: date
