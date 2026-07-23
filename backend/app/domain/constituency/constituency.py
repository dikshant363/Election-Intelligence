"""Constituency aggregate root."""

from app.domain.common.base import AggregateRoot
from app.domain.value_objects import ConstituencyId, StateCode


class Constituency(AggregateRoot[ConstituencyId]):
    """Constituency aggregate root representing an electoral region."""

    def __init__(
        self,
        id: ConstituencyId,
        name: str,
        code: str,
        state_code: StateCode,
        constituency_type: str = "ASSEMBLY",
    ) -> None:
        super().__init__(id)
        if not name or not name.strip():
            raise ValueError("Constituency name cannot be empty.")
        if not code or not code.strip():
            raise ValueError("Constituency code cannot be empty.")

        self.name = name
        self.code = code
        self.state_code = state_code
        self.constituency_type = constituency_type
