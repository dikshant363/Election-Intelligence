"""FastAPI router for /api/v1/parties endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, Request, status

from app.api.v1.dependencies import (
    get_command_pipeline,
    get_query_handlers,
)
from app.api.v1.errors import raise_result_failure
from app.api.v1.schemas import (
    PaginatedResponse,
    PaginationParams,
    PartyCreateRequest,
    PartyResponse,
)
from app.application.commands import RegisterParty
from app.application.handlers import QueryHandlers
from app.application.pipeline import CommandPipeline
from app.application.queries import GetParty, ListParties

router = APIRouter(prefix="/parties", tags=["Political Parties"])


@router.post(
    "",
    response_model=PartyResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new political party",
)
async def register_party(
    request: Request,
    body: PartyCreateRequest,
    pipeline: Annotated[CommandPipeline, Depends(get_command_pipeline)],
) -> PartyResponse:
    """Register political party via CQRS CommandPipeline."""
    cmd = RegisterParty(
        name=body.name,
        code=body.code,
        symbol=body.symbol,
    )
    result = await pipeline.execute_register_party(cmd)
    if result.is_failure:
        raise_result_failure(result, request.url.path)
    return PartyResponse.from_dto(result.unwrap())


@router.get(
    "/{party_id}",
    response_model=PartyResponse,
    status_code=status.HTTP_200_OK,
    summary="Get political party details by ID",
)
async def get_party(
    request: Request,
    party_id: str,
    query_handlers: Annotated[QueryHandlers, Depends(get_query_handlers)],
) -> PartyResponse:
    """Fetch a party by ID via QueryHandlers."""
    result = await query_handlers.handle_get_party(GetParty(id=party_id))
    if result.is_failure:
        raise_result_failure(result, request.url.path)
    return PartyResponse.from_dto(result.unwrap())


@router.get(
    "",
    response_model=PaginatedResponse[PartyResponse],
    status_code=status.HTTP_200_OK,
    summary="List political parties with pagination",
)
async def list_parties(
    request: Request,
    pagination: Annotated[PaginationParams, Depends()],
    query_handlers: Annotated[QueryHandlers, Depends(get_query_handlers)],
) -> PaginatedResponse[PartyResponse]:
    """List political parties via QueryHandlers."""
    query = ListParties(skip=pagination.skip, limit=pagination.size)
    result = await query_handlers.handle_list_parties(query)
    if result.is_failure:
        raise_result_failure(result, request.url.path)
    dtos = result.unwrap()
    items = [PartyResponse.from_dto(d) for d in dtos]
    total = len(items)
    pages = (total + pagination.size - 1) // pagination.size if total > 0 else 1
    return PaginatedResponse[PartyResponse](
        items=items,
        total=total,
        page=pagination.page,
        size=pagination.size,
        pages=pages,
    )
