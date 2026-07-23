"""Political Party application command objects."""

from dataclasses import dataclass


@dataclass(frozen=True)
class RegisterParty:
    """Command to register a new political party."""

    name: str
    code: str
    symbol: str
