"""Persistence models package initialization."""

from app.persistence.models.candidate import CandidateModel
from app.persistence.models.constituency import ConstituencyModel
from app.persistence.models.election import ElectionModel
from app.persistence.models.party import PoliticalPartyModel
from app.persistence.models.polling import PollingBoothModel
from app.persistence.models.results import ElectionResultModel

__all__ = [
    "CandidateModel",
    "ConstituencyModel",
    "ElectionModel",
    "PoliticalPartyModel",
    "PollingBoothModel",
    "ElectionResultModel",
]
