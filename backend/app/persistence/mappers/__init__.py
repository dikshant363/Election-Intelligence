"""Persistence mappers package initialization."""

from app.persistence.mappers.candidate_mapper import CandidateMapper
from app.persistence.mappers.constituency_mapper import ConstituencyMapper
from app.persistence.mappers.election_mapper import ElectionMapper
from app.persistence.mappers.party_mapper import PartyMapper
from app.persistence.mappers.polling_mapper import PollingMapper
from app.persistence.mappers.result_mapper import ResultMapper

__all__ = [
    "CandidateMapper",
    "ConstituencyMapper",
    "ElectionMapper",
    "PartyMapper",
    "PollingMapper",
    "ResultMapper",
]
