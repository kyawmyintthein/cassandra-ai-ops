from __future__ import annotations

from intake_service.api.schemas import SignalIngestRequest
from intake_service.domain.contracts import CanonicalSignal


def normalize_signal(request: SignalIngestRequest) -> CanonicalSignal:
    return CanonicalSignal(
        source=request.source,
        service=request.service,
        environment=request.environment,
        symptom_type=request.symptom_type,
        metric_name=request.metric_name,
        baseline_value=request.baseline_value,
        current_value=request.current_value,
        unit=request.unit,
        detected_at=request.detected_at,
    )

