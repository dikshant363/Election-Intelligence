"""FastAPI router for /api/v1/constituencies endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request, status

from app.api.v1.dependencies import (
    get_command_pipeline,
    get_query_handlers,
)
from app.api.v1.errors import raise_result_failure
from app.api.v1.schemas import (
    ConstituencyCreateRequest,
    ConstituencyResponse,
    PaginatedResponse,
    PaginationParams,
)
from app.application.commands import CreateConstituency
from app.application.handlers import QueryHandlers
from app.application.pipeline import CommandPipeline
from app.application.queries import GetConstituency, ListConstituencies

router = APIRouter(prefix="/constituencies", tags=["Constituencies"])


@router.post(
    "",
    response_model=ConstituencyResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new electoral constituency",
)
async def create_constituency(
    request: Request,
    body: ConstituencyCreateRequest,
    pipeline: Annotated[CommandPipeline, Depends(get_command_pipeline)],
) -> ConstituencyResponse:
    """Create a new constituency via CQRS CommandPipeline."""
    cmd = CreateConstituency(
        name=body.name,
        code=body.code,
        state_code=body.state_code,
        constituency_type=body.constituency_type,
    )
    result = await pipeline.execute_create_constituency(cmd)
    if result.is_failure:
        raise_result_failure(result, request.url.path)
    return ConstituencyResponse.from_dto(result.unwrap())


@router.get(
    "",
    response_model=PaginatedResponse[ConstituencyResponse],
    status_code=status.HTTP_200_OK,
    summary="List electoral constituencies with optional filtering and pagination",
)
async def list_constituencies(
    request: Request,
    pagination: Annotated[PaginationParams, Depends()],
    query_handlers: Annotated[QueryHandlers, Depends(get_query_handlers)],
    state_code: Annotated[str | None, Query()] = None,
) -> PaginatedResponse[ConstituencyResponse]:
    """List constituencies via QueryHandlers."""
    query = ListConstituencies(
        state_code=state_code,
        skip=pagination.skip,
        limit=pagination.size,
    )
    result = await query_handlers.handle_list_constituencies(query)
    if result.is_failure:
        raise_result_failure(result, request.url.path)
    dtos = result.unwrap()
    items = [ConstituencyResponse.from_dto(d) for d in dtos]
    total = len(items)
    pages = (total + pagination.size - 1) // pagination.size if total > 0 else 1
    return PaginatedResponse[ConstituencyResponse](
        items=items,
        total=total,
        page=pagination.page,
        size=pagination.size,
        pages=pages,
    )


@router.get(
    "/{constituency_id}",
    response_model=ConstituencyResponse,
    status_code=status.HTTP_200_OK,
    summary="Get constituency details by ID",
)
async def get_constituency(
    request: Request,
    constituency_id: str,
    query_handlers: Annotated[QueryHandlers, Depends(get_query_handlers)],
) -> ConstituencyResponse:
    """Fetch a constituency by ID via QueryHandlers."""
    result = await query_handlers.handle_get_constituency(
        GetConstituency(id=constituency_id)
    )
    if result.is_failure:
        raise_result_failure(result, request.url.path)
    return ConstituencyResponse.from_dto(result.unwrap())
