from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from intake_service.api.schemas import SignalIngestRequest
from intake_service.application.intake_service import IntakeService
from intake_service.domain.contracts import QueueEvent
from intake_service.domain.enums import SignalSource
from intake_service.infrastructure.db.models import Base, RawSignalModel
from intake_service.infrastructure.db.repositories import IntakeRepository
from intake_service.infrastructure.queue.base import QueueBackend


class FakeQueueBackend(QueueBackend):
    def __init__(self) -> None:
        self.published: list[QueueEvent] = []

    def publish(self, event: QueueEvent) -> None:
        self.published.append(event)

    def consume(self, topic: str, batch_size: int) -> list:
        return []

    def acknowledge(self, message_id: UUID) -> None:
        return None

    def retry(self, message_id: UUID, error: str) -> None:
        return None


def test_ingest_signal_serializes_raw_payload_to_json_safe_values() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
    queue = FakeQueueBackend()

    request = SignalIngestRequest(
        source=SignalSource.OBSERVABILITY_WEBHOOK,
        detected_at=datetime(2026, 4, 8, 4, 30, tzinfo=UTC),
        service="checkout",
        environment="prod",
        symptom_type="latency_spike",
        metric_name="p99_latency",
        baseline_value=200.0,
        current_value=900.0,
        unit="ms",
        payload={"reported_at": datetime(2026, 4, 8, 4, 31, tzinfo=UTC)},
    )

    with Session() as session:
        service = IntakeService(session, queue)
        response = service.ingest_signal(request)

        raw_signal = session.get(RawSignalModel, response.raw_signal_id)

        assert raw_signal is not None
        assert raw_signal.payload["attributes"]["detected_at"] == "2026-04-08T04:30:00+00:00"
        assert raw_signal.payload["payload"]["reported_at"] == "2026-04-08T04:31:00+00:00"
        assert queue.published[0].topic == "signal.assessment.requested"
