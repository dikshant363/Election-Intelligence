"""FastAPI router for /api/v1/polling-booths endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, Request, status

from app.api.v1.dependencies import get_command_pipeline
from app.api.v1.errors import raise_result_failure
from app.api.v1.schemas import (
    PollingBoothCreateRequest,
    PollingBoothResponse,
)
from app.application.commands import CreatePollingBooth
from app.application.pipeline import CommandPipeline

router = APIRouter(prefix="/polling-booths", tags=["Polling Booths"])


@router.post(
    "",
    response_model=PollingBoothResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Establish a new polling booth",
)
async def create_polling_booth(
    request: Request,
    body: PollingBoothCreateRequest,
    pipeline: Annotated[CommandPipeline, Depends(get_command_pipeline)],
) -> PollingBoothResponse:
    """Establish a new polling booth station via CQRS CommandPipeline."""
    cmd = CreatePollingBooth(
        constituency_id=body.constituency_id,
        booth_name=body.booth_name,
        booth_number=body.booth_number,
        latitude=body.latitude,
        longitude=body.longitude,
    )
    result = await pipeline.execute_create_polling_booth(cmd)
    if result.is_failure:
        raise_result_failure(result, request.url.path)
    return PollingBoothResponse.from_dto(result.unwrap())
