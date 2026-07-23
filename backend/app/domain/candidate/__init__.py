"""Candidate package initialization."""

from app.domain.candidate.candidate import Candidate, CandidateRegistered
from app.domain.candidate.repository import CandidateRepository

__all__ = ["Candidate", "CandidateRegistered", "CandidateRepository"]
