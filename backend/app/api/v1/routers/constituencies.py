"""FastAPI router for /api/v1/constituencies endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, Request, status

from app.api.v1.dependencies import (
    get_command_pipeline,
    get_query_handlers,
)
from app.api.v1.errors import raise_result_failure
from app.api.v1.schemas import (
    ConstituencyCreateRequest,
    ConstituencyResponse,
)
from app.application.commands import CreateConstituency
from app.application.handlers import QueryHandlers
from app.application.pipeline import CommandPipeline
from app.application.queries import GetConstituency

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
