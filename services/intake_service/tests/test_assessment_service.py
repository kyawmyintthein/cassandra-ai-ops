from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from intake_service.api.schemas import AssessmentResultRequest
from intake_service.application.assessment_service import AssessmentService
from intake_service.domain.contracts import CanonicalSignal, QueueEvent
from intake_service.domain.enums import Classification, SignalSource
from intake_service.infrastructure.db.models import Base
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


def test_incident_result_creates_investigation_without_incident() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
    queue = FakeQueueBackend()

    with Session() as session:
        repo = IntakeRepository(session)
        with session.begin():
            raw_signal = repo.create_raw_signal(
                SignalSource.USER.value,
                {"payload": {"message": "error budget burn"}, "attributes": {}},
            )
            signal = repo.create_signal(
                raw_signal.id,
                signal=CanonicalSignal(
                    source=SignalSource.USER,
                    service="checkout",
                    environment="prod",
                    symptom_type="latency_spike",
                    metric_name="p99_latency",
                    baseline_value=200.0,
                    current_value=700.0,
                    unit="ms",
                    detected_at=datetime(2026, 4, 8, 3, 0, tzinfo=UTC),
                ),
            )

        request = AssessmentResultRequest(
            event_id="evt-1",
            signal_id=signal.id,
            classification=Classification.INCIDENT,
            reason="Material customer impact observed",
        )

        service = AssessmentService(session, queue)
        service.process_result(request)

        persisted_signal = repo.get_signal(signal.id)
        incident = repo.get_incident_for_signal(signal.id)
        investigation = repo.get_investigation_for_signal(signal.id)

        assert persisted_signal is not None
        assert persisted_signal.workflow_state == "investigation_requested"
        assert persisted_signal.classification == "incident"
        assert incident is None
        assert investigation is not None
        assert queue.published[0].topic == "investigation.requested"
