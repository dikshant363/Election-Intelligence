"""Application DTOs package initialization."""

from app.application.dto.candidate_dto import CandidateDTO
from app.application.dto.constituency_dto import ConstituencyDTO
from app.application.dto.election_dto import ElectionDTO
from app.application.dto.party_dto import PartyDTO
from app.application.dto.polling_dto import PollingBoothDTO
from app.application.dto.results_dto import ElectionResultDTO

__all__ = [
    "CandidateDTO",
    "ConstituencyDTO",
    "ElectionDTO",
    "PartyDTO",
    "PollingBoothDTO",
    "ElectionResultDTO",
]
