"""Presence management tracking client connections, topics, and idle timeouts."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class ClientPresence:
    """Client presence record."""

    client_id: str
    user_id: str | None = None
    connected_at: str = field(
        default_factory=lambda: datetime.now(UTC).isoformat()
    )
    last_heartbeat: str = field(
        default_factory=lambda: datetime.now(UTC).isoformat()
    )
    topics: set[str] = field(default_factory=set)

    def update_heartbeat(self) -> None:
        self.last_heartbeat = datetime.now(UTC).isoformat()


class PresenceManager:
    """Tracks connected clients, active subscriptions, and heartbeats."""

    def __init__(self) -> None:
        self._clients: dict[str, ClientPresence] = {}

    def register(self, client_id: str, user_id: str | None = None) -> ClientPresence:
        p = ClientPresence(client_id=client_id, user_id=user_id)
        self._clients[client_id] = p
        return p

    def unregister(self, client_id: str) -> None:
        self._clients.pop(client_id, None)

    def get(self, client_id: str) -> ClientPresence | None:
        return self._clients.get(client_id)

    def subscribe_topic(self, client_id: str, topic: str) -> None:
        p = self._clients.get(client_id)
        if p:
            p.topics.add(topic)

    def unsubscribe_topic(self, client_id: str, topic: str) -> None:
        p = self._clients.get(client_id)
        if p:
            p.topics.discard(topic)

    def update_heartbeat(self, client_id: str) -> None:
        p = self._clients.get(client_id)
        if p:
            p.update_heartbeat()

    def count(self) -> int:
        return len(self._clients)

    def list_presence(self) -> list[ClientPresence]:
        return list(self._clients.values())
