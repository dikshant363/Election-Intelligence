"""FastAPI router for real-time events, SSE streaming, and WebSocket channels."""

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect, status
from fastapi.responses import StreamingResponse

from app.api.v1.dependencies.dependencies import get_realtime_service
from app.realtime.events import EventEnvelope
from app.realtime.schemas import (
    EventEnvelopeSchema,
    PresenceInfoSchema,
    PublishEventRequestSchema,
    RealtimeMetricsSchema,
)
from app.realtime.services import RealtimeService
from app.realtime.streaming import sse_event_generator

router = APIRouter(tags=["Real-Time Intelligence"])


@router.get(
    "/events",
    response_model=list[EventEnvelopeSchema],
    status_code=status.HTTP_200_OK,
    summary="Replay historical events for a topic",
)
async def replay_events(
    topic: Annotated[str, Query(description="Topic channel name")],
    from_timestamp: Annotated[str | None, Query(description="ISO timestamp filter")] = None,
    realtime_service: Annotated[RealtimeService, Depends(get_realtime_service)] = None,
) -> list[EventEnvelopeSchema]:
    """Replay historical EventEnvelope list from EventBus event log."""
    events = realtime_service.replay_events(topic=topic, from_timestamp=from_timestamp)
    return [EventEnvelopeSchema(**e.to_dict()) for e in events]


@router.get(
    "/stream",
    status_code=status.HTTP_200_OK,
    summary="Subscribe to Server-Sent Events (SSE) topic stream",
)
async def sse_stream(
    topic: Annotated[str, Query(description="Topic channel name")],
    realtime_service: Annotated[RealtimeService, Depends(get_realtime_service)] = None,
) -> StreamingResponse:
    """Stream live Server-Sent Events (SSE) for specified topic."""
    gen = sse_event_generator(realtime_service.stream_topic(topic))
    return StreamingResponse(gen, media_type="text/event-stream")


@router.post(
    "/events/publish",
    response_model=EventEnvelopeSchema,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Publish custom event to EventBus and connected clients",
)
async def publish_event(
    body: PublishEventRequestSchema,
    realtime_service: Annotated[RealtimeService, Depends(get_realtime_service)],
) -> EventEnvelopeSchema:
    """Publish custom event to target topic channel."""
    event = EventEnvelope(
        event_type=body.event_type,
        aggregate_id=body.aggregate_id,
        payload=body.payload,
    )
    await realtime_service.publish_event(topic=body.topic, event=event)
    return EventEnvelopeSchema(**event.to_dict())


@router.get(
    "/realtime/presence",
    response_model=list[PresenceInfoSchema],
    status_code=status.HTTP_200_OK,
    summary="List connected client presence",
)
async def presence(
    realtime_service: Annotated[RealtimeService, Depends(get_realtime_service)],
) -> list[PresenceInfoSchema]:
    """List connected WebSocket client presence status."""
    return realtime_service.list_presence()


@router.get(
    "/realtime/metrics",
    response_model=RealtimeMetricsSchema,
    status_code=status.HTTP_200_OK,
    summary="Get real-time system performance metrics",
)
async def metrics(
    realtime_service: Annotated[RealtimeService, Depends(get_realtime_service)],
) -> RealtimeMetricsSchema:
    """Get connected client count, throughput, dropped messages, and latency metrics."""
    return realtime_service.get_metrics()


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    realtime_service: Annotated[RealtimeService, Depends(get_realtime_service)],
) -> None:
    """WebSocket endpoint for real-time bi-directional topic streaming."""
    client_id = str(uuid.uuid4())
    await realtime_service.connection_manager.connect(client_id, websocket)

    try:
        while True:
            data = await websocket.receive_json()
            action = data.get("action")
            topic = data.get("topic")

            if action == "subscribe" and topic:
                realtime_service.connection_manager.subscribe(client_id, topic)
                await websocket.send_json({"status": "subscribed", "topic": topic})
            elif action == "unsubscribe" and topic:
                realtime_service.connection_manager.unsubscribe(client_id, topic)
                await websocket.send_json({"status": "unsubscribed", "topic": topic})
            elif action == "ping":
                await websocket.send_json({"type": "pong"})
    except WebSocketDisconnect:
        realtime_service.connection_manager.disconnect(client_id)
