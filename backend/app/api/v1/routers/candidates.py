"""FastAPI router for /api/v1/candidates endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request, status

from app.api.v1.dependencies import (
    get_command_pipeline,
    get_query_handlers,
)
from app.api.v1.errors import raise_result_failure
from app.api.v1.schemas import (
    CandidateCreateRequest,
    CandidateResponse,
    PaginatedResponse,
    PaginationParams,
)
from app.application.commands import RegisterCandidate
from app.application.handlers import QueryHandlers
from app.application.pipeline import CommandPipeline
from app.application.queries import GetCandidate, ListCandidates

router = APIRouter(prefix="/candidates", tags=["Candidates"])


@router.post(
    "",
    response_model=CandidateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new candidate",
)
async def register_candidate(
    request: Request,
    body: CandidateCreateRequest,
    pipeline: Annotated[CommandPipeline, Depends(get_command_pipeline)],
) -> CandidateResponse:
    """Register candidate via CQRS CommandPipeline."""
    cmd = RegisterCandidate(
        name=body.name,
        age=body.age,
        email=body.email,
        phone=body.phone,
        constituency_id=body.constituency_id,
        party_id=body.party_id,
    )
    result = await pipeline.execute_register_candidate(cmd)
    if result.is_failure:
        raise_result_failure(result, request.url.path)
    return CandidateResponse.from_dto(result.unwrap())


@router.get(
    "/{candidate_id}",
    response_model=CandidateResponse,
    status_code=status.HTTP_200_OK,
    summary="Get candidate details by ID",
)
async def get_candidate(
    request: Request,
    candidate_id: str,
    query_handlers: Annotated[QueryHandlers, Depends(get_query_handlers)],
) -> CandidateResponse:
    """Fetch candidate details by ID via QueryHandlers."""
    result = await query_handlers.handle_get_candidate(GetCandidate(id=candidate_id))
    if result.is_failure:
        raise_result_failure(result, request.url.path)
    return CandidateResponse.from_dto(result.unwrap())


@router.get(
    "",
    response_model=PaginatedResponse[CandidateResponse],
    status_code=status.HTTP_200_OK,
    summary="List candidates with optional filtering and pagination",
)
async def list_candidates(
    request: Request,
    pagination: Annotated[PaginationParams, Depends()],
    query_handlers: Annotated[QueryHandlers, Depends(get_query_handlers)],
    constituency_id: Annotated[str | None, Query()] = None,
    party_id: Annotated[str | None, Query()] = None,
) -> PaginatedResponse[CandidateResponse]:
    """List candidates via QueryHandlers."""
    query = ListCandidates(
        constituency_id=constituency_id,
        party_id=party_id,
        skip=pagination.skip,
        limit=pagination.size,
    )
    result = await query_handlers.handle_list_candidates(query)
    if result.is_failure:
        raise_result_failure(result, request.url.path)
    dtos = result.unwrap()
    items = [CandidateResponse.from_dto(d) for d in dtos]
    total = len(items)
    pages = (total + pagination.size - 1) // pagination.size if total > 0 else 1
    return PaginatedResponse[CandidateResponse](
        items=items,
        total=total,
        page=pagination.page,
        size=pagination.size,
        pages=pages,
    )
