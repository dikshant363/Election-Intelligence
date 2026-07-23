"""Domain Events and EventEnvelope standard specification."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(frozen=True)
class EventEnvelope:
    """Standardized Event Envelope for vendor-independent messaging & replay."""

    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str = "DomainEvent"
    event_version: str = "v1.0"
    aggregate_id: str = ""
    timestamp: str = field(
        default_factory=lambda: datetime.now(UTC).isoformat()
    )
    correlation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    causation_id: str = ""
    producer: str = "election-intelligence-platform"
    payload: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize envelope to dictionary."""
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "event_version": self.event_version,
            "aggregate_id": self.aggregate_id,
            "timestamp": self.timestamp,
            "correlation_id": self.correlation_id,
            "causation_id": self.causation_id,
            "producer": self.producer,
            "payload": self.payload,
            "metadata": self.metadata,
        }


# ─────────────────────────────────────────────────────────────────────────────
# Immutable Domain Event Constructors
# ─────────────────────────────────────────────────────────────────────────────


def create_election_created_event(election_id: str, title: str, election_type: str) -> EventEnvelope:
    return EventEnvelope(
        event_type="ElectionCreated",
        aggregate_id=election_id,
        payload={"election_id": election_id, "title": title, "election_type": election_type},
    )


def create_election_updated_event(election_id: str, status: str) -> EventEnvelope:
    return EventEnvelope(
        event_type="ElectionUpdated",
        aggregate_id=election_id,
        payload={"election_id": election_id, "status": status},
    )


def create_result_published_event(result_id: str, election_id: str, candidate_id: str, votes: int) -> EventEnvelope:
    return EventEnvelope(
        event_type="ResultPublished",
        aggregate_id=result_id,
        payload={
            "result_id": result_id,
            "election_id": election_id,
            "candidate_id": candidate_id,
            "votes": votes,
        },
    )


def create_candidate_updated_event(candidate_id: str, name: str) -> EventEnvelope:
    return EventEnvelope(
        event_type="CandidateUpdated",
        aggregate_id=candidate_id,
        payload={"candidate_id": candidate_id, "name": name},
    )


def create_party_updated_event(party_id: str, name: str, code: str) -> EventEnvelope:
    return EventEnvelope(
        event_type="PartyUpdated",
        aggregate_id=party_id,
        payload={"party_id": party_id, "name": name, "code": code},
    )


def create_polling_booth_updated_event(booth_id: str, name: str, state_code: str) -> EventEnvelope:
    return EventEnvelope(
        event_type="PollingBoothUpdated",
        aggregate_id=booth_id,
        payload={"booth_id": booth_id, "name": name, "state_code": state_code},
    )


def create_import_completed_event(job_id: str, record_count: int) -> EventEnvelope:
    return EventEnvelope(
        event_type="ImportCompleted",
        aggregate_id=job_id,
        payload={"job_id": job_id, "record_count": record_count},
    )


def create_search_index_updated_event(index_name: str, doc_count: int) -> EventEnvelope:
    return EventEnvelope(
        event_type="SearchIndexUpdated",
        aggregate_id=index_name,
        payload={"index_name": index_name, "doc_count": doc_count},
    )


def create_ai_evaluation_completed_event(eval_id: str, grounding_score: float) -> EventEnvelope:
    return EventEnvelope(
        event_type="AIEvaluationCompleted",
        aggregate_id=eval_id,
        payload={"eval_id": eval_id, "grounding_score": grounding_score},
    )
