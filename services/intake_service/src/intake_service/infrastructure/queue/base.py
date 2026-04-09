from __future__ import annotations

from intake_service.domain.contracts import EventPublisher, QueueConsumer


class QueueBackend(EventPublisher, QueueConsumer):
    """Marker base class for queue backends used by the intake service."""

