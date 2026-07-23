"""Persistence repositories package initialization."""

from app.persistence.repositories.candidate_repository import (
    SqlAlchemyCandidateRepository,
)
from app.persistence.repositories.constituency_repository import (
    SqlAlchemyConstituencyRepository,
)
from app.persistence.repositories.election_repository import (
    SqlAlchemyElectionRepository,
)
from app.persistence.repositories.party_repository import (
    SqlAlchemyPartyRepository,
)
from app.persistence.repositories.polling_repository import (
    SqlAlchemyPollingRepository,
)
from app.persistence.repositories.result_repository import (
    SqlAlchemyResultRepository,
)

__all__ = [
    "SqlAlchemyCandidateRepository",
    "SqlAlchemyConstituencyRepository",
    "SqlAlchemyElectionRepository",
    "SqlAlchemyPartyRepository",
    "SqlAlchemyPollingRepository",
    "SqlAlchemyResultRepository",
]
