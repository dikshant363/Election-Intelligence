"""FastAPI router for /api/v1/elections endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request, status

from app.api.v1.dependencies import (
    get_command_pipeline,
    get_query_handlers,
)
from app.api.v1.errors import raise_result_failure
from app.api.v1.schemas import (
    ElectionCreateRequest,
    ElectionResponse,
    PaginatedResponse,
    PaginationParams,
)
from app.application.commands import CreateElection
from app.application.handlers import QueryHandlers
from app.application.pipeline import CommandPipeline
from app.application.queries import GetElection, ListElections
from app.domain.value_objects import ElectionType

router = APIRouter(prefix="/elections", tags=["Elections"])


@router.post(
    "",
    response_model=ElectionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Schedule a new election",
)
async def create_election(
    request: Request,
    body: ElectionCreateRequest,
    pipeline: Annotated[CommandPipeline, Depends(get_command_pipeline)],
) -> ElectionResponse:
    """Create a new election via CQRS CommandPipeline."""
    cmd = CreateElection(
        title=body.title,
        election_type=ElectionType(body.election_type),
        start_date=body.start_date,
        end_date=body.end_date,
    )
    result = await pipeline.execute_create_election(cmd)
    if result.is_failure:
        raise_result_failure(result, request.url.path)
    return ElectionResponse.from_dto(result.unwrap())


@router.get(
    "/{election_id}",
    response_model=ElectionResponse,
    status_code=status.HTTP_200_OK,
    summary="Get election details by ID",
)
async def get_election(
    request: Request,
    election_id: str,
    query_handlers: Annotated[QueryHandlers, Depends(get_query_handlers)],
) -> ElectionResponse:
    """Fetch an election by ID via QueryHandlers."""
    result = await query_handlers.handle_get_election(GetElection(id=election_id))
    if result.is_failure:
        raise_result_failure(result, request.url.path)
    return ElectionResponse.from_dto(result.unwrap())


@router.get(
    "",
    response_model=PaginatedResponse[ElectionResponse],
    status_code=status.HTTP_200_OK,
    summary="List elections with pagination",
)
async def list_elections(
    request: Request,
    pagination: Annotated[PaginationParams, Depends()],
    query_handlers: Annotated[QueryHandlers, Depends(get_query_handlers)],
    status_filter: Annotated[str | None, Query(alias="status")] = None,
) -> PaginatedResponse[ElectionResponse]:
    """List elections with pagination via QueryHandlers."""
    query = ListElections(
        status=status_filter,
        skip=pagination.skip,
        limit=pagination.size,
    )
    result = await query_handlers.handle_list_elections(query)
    if result.is_failure:
        raise_result_failure(result, request.url.path)
    dtos = result.unwrap()
    items = [ElectionResponse.from_dto(d) for d in dtos]
    total = len(items)
    pages = (total + pagination.size - 1) // pagination.size if total > 0 else 1
    return PaginatedResponse[ElectionResponse](
        items=items,
        total=total,
        page=pagination.page,
        size=pagination.size,
        pages=pages,
    )
