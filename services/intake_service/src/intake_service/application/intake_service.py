from __future__ import annotations

from uuid import UUID, uuid4

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from intake_service.api.schemas import SignalIngestRequest, SignalIngestResponse
from intake_service.application.normalization import normalize_signal
from intake_service.domain.contracts import QueueEvent
from intake_service.domain.enums import WorkflowState
from intake_service.infrastructure.db.repositories import IntakeRepository
from intake_service.infrastructure.queue.base import QueueBackend


class IntakeService:
    def __init__(self, session: Session, queue_backend: QueueBackend) -> None:
        self.session = session
        self.repository = IntakeRepository(session)
        self.queue_backend = queue_backend

    def ingest_signal(self, request: SignalIngestRequest) -> SignalIngestResponse:
        raw_payload = jsonable_encoder(
            {
                "payload": request.payload,
                "attributes": request.model_dump(exclude={"payload"}),
            }
        )
        signal = normalize_signal(request)

        with self.session.begin():
            raw_signal = self.repository.create_raw_signal(request.source.value, raw_payload)
            signal_model = self.repository.create_signal(raw_signal.id, signal)

        self.queue_backend.publish(
            QueueEvent(
                event_id=str(uuid4()),
                topic="signal.assessment.requested",
                payload={
                    "signal_id": signal_model.id,
                    "source": signal_model.source,
                    "service": signal_model.service,
                    "environment": signal_model.environment,
                    "symptom_type": signal_model.symptom_type,
                    "metric_name": signal_model.metric_name,
                    "baseline_value": signal_model.baseline_value,
                    "current_value": signal_model.current_value,
                    "unit": signal_model.unit,
                    "detected_at": signal_model.detected_at.isoformat(),
                },
            )
        )

        return SignalIngestResponse(
            signal_id=signal_model.id,
            raw_signal_id=raw_signal.id,
            workflow_state=WorkflowState(signal_model.workflow_state),
        )
