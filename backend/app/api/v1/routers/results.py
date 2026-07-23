"""FastAPI router for /api/v1/results endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request, status

from app.api.v1.dependencies import (
    get_command_pipeline,
    get_query_handlers,
)
from app.api.v1.errors import raise_result_failure
from app.api.v1.schemas import (
    ElectionResultRequest,
    ElectionResultResponse,
)
from app.application.commands import DeclareResult
from app.application.handlers import QueryHandlers
from app.application.pipeline import CommandPipeline
from app.application.queries import GetResult

router = APIRouter(prefix="/results", tags=["Election Results"])


@router.post(
    "",
    response_model=ElectionResultResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Declare election result for a constituency",
)
async def declare_result(
    request: Request,
    body: ElectionResultRequest,
    pipeline: Annotated[CommandPipeline, Depends(get_command_pipeline)],
) -> ElectionResultResponse:
    """Declare constituency election result via CQRS CommandPipeline."""
    cmd = DeclareResult(
        election_id=body.election_id,
        constituency_id=body.constituency_id,
        candidate_votes=body.candidate_votes,
        winning_candidate_id=body.winning_candidate_id,
    )
    result = await pipeline.execute_declare_result(cmd)
    if result.is_failure:
        raise_result_failure(result, request.url.path)
    return ElectionResultResponse.from_dto(result.unwrap())


@router.get(
    "",
    response_model=ElectionResultResponse,
    status_code=status.HTTP_200_OK,
    summary="Get constituency election result details",
)
async def get_result(
    request: Request,
    election_id: Annotated[str, Query()],
    constituency_id: Annotated[str, Query()],
    query_handlers: Annotated[QueryHandlers, Depends(get_query_handlers)],
) -> ElectionResultResponse:
    """Fetch election result via QueryHandlers."""
    result = await query_handlers.handle_get_result(
        GetResult(election_id=election_id, constituency_id=constituency_id)
    )
    if result.is_failure:
        raise_result_failure(result, request.url.path)
    return ElectionResultResponse.from_dto(result.unwrap())
