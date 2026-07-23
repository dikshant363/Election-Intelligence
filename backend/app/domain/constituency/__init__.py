"""Constituency package initialization."""

from app.domain.constituency.constituency import Constituency
from app.domain.constituency.repository import ConstituencyRepository

__all__ = ["Constituency", "ConstituencyRepository"]
