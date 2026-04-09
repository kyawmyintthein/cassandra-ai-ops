from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy.orm import Session

from intake_service.api.schemas import AssessmentResultRequest
from intake_service.domain.contracts import QueueEvent
from intake_service.domain.enums import Classification
from intake_service.infrastructure.db.repositories import IntakeRepository
from intake_service.infrastructure.queue.base import QueueBackend


class AssessmentService:
    def __init__(self, session: Session, queue_backend: QueueBackend) -> None:
        self.session = session
        self.repository = IntakeRepository(session)
        self.queue_backend = queue_backend

    def process_result(self, result: AssessmentResultRequest) -> None:
        with self.session.begin():
            if self.repository.event_already_processed(result.event_id):
                return

            signal = self.repository.get_signal(result.signal_id)
            if signal is None:
                raise ValueError(f"Signal {result.signal_id} was not found")

            if result.classification == Classification.ALERT:
                self.repository.mark_alert(signal, result.classification, result.reason)
            else:
                self.repository.mark_promoted_for_investigation(signal, result.classification, result.reason)
                investigation = self.repository.get_investigation_for_signal(signal.id)
                if investigation is None:
                    investigation = self.repository.create_investigation(signal.id)
                    self.queue_backend.publish(
                        QueueEvent(
                            event_id=str(uuid4()),
                            topic="investigation.requested",
                            payload={
                                "investigation_id": str(investigation.id),
                                "signal_id": str(signal.id),
                                "requested_at": datetime.now(UTC).isoformat(),
                            },
                        )
                    )

            self.repository.record_processed_event(result.event_id, "signal.assessed")
