"""Results package initialization."""

from app.domain.results.repository import ResultRepository
from app.domain.results.results import ElectionResult, ResultDeclared

__all__ = ["ElectionResult", "ResultDeclared", "ResultRepository"]
