"""Constituency application command objects."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CreateConstituency:
    """Command to establish a new electoral constituency."""

    name: str
    code: str
    state_code: str
    constituency_type: str = "ASSEMBLY"
