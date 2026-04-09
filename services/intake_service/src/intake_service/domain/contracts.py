from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Protocol
from uuid import UUID

from intake_service.domain.enums import Classification, SignalSource, Severity


@dataclass(frozen=True)
class CanonicalSignal:
    """Normalized signal payload used by intake workflow and downstream events."""

    source: SignalSource
    service: str | None
    environment: str | None
    symptom_type: str | None
    metric_name: str | None
    baseline_value: float | None
    current_value: float | None
    unit: str | None
    detected_at: datetime


@dataclass(frozen=True)
class QueueEvent:
    event_id: str
    topic: str
    payload: dict[str, Any]


@dataclass(frozen=True)
class IncidentProjection:
    signal_id: str
    severity: Severity
    window_start: datetime
    window_end: datetime


@dataclass(frozen=True)
class QueueMessage:
    id: UUID
    topic: str
    payload: dict[str, Any]
    attempt_count: int


class EventPublisher(Protocol):
    def publish(self, event: QueueEvent) -> None:
        """Publish an event to the queue backend."""


class QueueConsumer(Protocol):
    def consume(self, topic: str, batch_size: int) -> list[QueueMessage]:
        """Fetch a batch of messages ready for processing."""

    def acknowledge(self, message_id: UUID) -> None:
        """Mark the message as completed."""

    def retry(self, message_id: UUID, error: str) -> None:
        """Requeue the message after a processing failure."""
