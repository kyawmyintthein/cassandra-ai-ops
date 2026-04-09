from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy.orm import Session

from intake_service.domain.contracts import CanonicalSignal
from intake_service.domain.enums import Classification, InvestigationStatus, WorkflowState
from intake_service.infrastructure.db.models import (
    IncidentModel,
    InvestigationModel,
    ProcessedEventModel,
    RawSignalModel,
    SignalModel,
)


class IntakeRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_raw_signal(self, source: str, payload: dict) -> RawSignalModel:
        raw_signal = RawSignalModel(source=source, payload=payload)
        self.session.add(raw_signal)
        self.session.flush()
        return raw_signal

    def create_signal(self, raw_signal_id: UUID, signal: CanonicalSignal) -> SignalModel:
        signal_model = SignalModel(
            raw_signal_id=raw_signal_id,
            source=signal.source.value,
            service=signal.service,
            environment=signal.environment,
            symptom_type=signal.symptom_type,
            metric_name=signal.metric_name,
            baseline_value=signal.baseline_value,
            current_value=signal.current_value,
            unit=signal.unit,
            detected_at=signal.detected_at,
            workflow_state=WorkflowState.ASSESSMENT_REQUESTED.value,
        )
        self.session.add(signal_model)
        self.session.flush()
        return signal_model

    def get_signal(self, signal_id: UUID) -> SignalModel | None:
        return self.session.get(SignalModel, signal_id)

    def mark_alert(self, signal: SignalModel, classification: Classification, reason: str | None) -> SignalModel:
        signal.classification = classification.value
        signal.classification_reason = reason
        signal.workflow_state = WorkflowState.ALERT.value
        signal.assessment_completed_at = datetime.now(UTC)
        self.session.flush()
        return signal

    def mark_promoted_for_investigation(
        self,
        signal: SignalModel,
        classification: Classification,
        reason: str | None,
    ) -> SignalModel:
        signal.classification = classification.value
        signal.classification_reason = reason
        signal.workflow_state = WorkflowState.INVESTIGATION_REQUESTED.value
        signal.assessment_completed_at = datetime.now(UTC)
        self.session.flush()
        return signal

    def create_investigation(self, signal_id: UUID) -> InvestigationModel:
        investigation = InvestigationModel(
            signal_id=signal_id,
            status=InvestigationStatus.REQUESTED.value,
        )
        self.session.add(investigation)
        self.session.flush()
        return investigation

    def get_incident_for_signal(self, signal_id: UUID) -> IncidentModel | None:
        return self.session.query(IncidentModel).filter(IncidentModel.signal_id == signal_id).one_or_none()

    def get_investigation_for_signal(self, signal_id: UUID) -> InvestigationModel | None:
        return self.session.query(InvestigationModel).filter(InvestigationModel.signal_id == signal_id).one_or_none()

    def event_already_processed(self, event_id: str) -> bool:
        return self.session.get(ProcessedEventModel, event_id) is not None

    def record_processed_event(self, event_id: str, topic: str) -> None:
        self.session.add(ProcessedEventModel(event_id=event_id, topic=topic))
        self.session.flush()
