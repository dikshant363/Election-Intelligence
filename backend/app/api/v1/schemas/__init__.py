"""API v1 schemas package initialization."""

from app.api.v1.schemas.candidate_schemas import (
    CandidateCreateRequest,
    CandidateResponse,
)
from app.api.v1.schemas.constituency_schemas import (
    ConstituencyCreateRequest,
    ConstituencyResponse,
)
from app.api.v1.schemas.election_schemas import (
    ElectionCreateRequest,
    ElectionResponse,
)
from app.api.v1.schemas.pagination import PaginatedResponse, PaginationParams
from app.api.v1.schemas.party_schemas import PartyCreateRequest, PartyResponse
from app.api.v1.schemas.polling_schemas import (
    PollingBoothCreateRequest,
    PollingBoothResponse,
)
from app.api.v1.schemas.result_schemas import (
    ElectionResultRequest,
    ElectionResultResponse,
)

__all__ = [
    "CandidateCreateRequest",
    "CandidateResponse",
    "ConstituencyCreateRequest",
    "ConstituencyResponse",
    "ElectionCreateRequest",
    "ElectionResponse",
    "ElectionResultRequest",
    "ElectionResultResponse",
    "PaginatedResponse",
    "PaginationParams",
    "PartyCreateRequest",
    "PartyResponse",
    "PollingBoothCreateRequest",
    "PollingBoothResponse",
]
