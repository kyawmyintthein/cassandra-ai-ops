from __future__ import annotations

from datetime import UTC, datetime

from intake_service.api.schemas import SignalIngestRequest
from intake_service.application.normalization import normalize_signal
from intake_service.domain.enums import SignalSource


def test_normalize_signal_preserves_canonical_fields() -> None:
    request = SignalIngestRequest(
        source=SignalSource.ANOMALY_DETECTION,
        detected_at=datetime(2026, 4, 8, 1, 2, tzinfo=UTC),
        service="payments",
        environment="prod",
        symptom_type="latency_spike",
        metric_name="p99_latency",
        baseline_value=250,
        current_value=1200,
        unit="ms",
        payload={"provider": "detector-a"},
    )

    signal = normalize_signal(request)

    assert signal.source == SignalSource.ANOMALY_DETECTION
    assert signal.service == "payments"
    assert signal.environment == "prod"
    assert signal.symptom_type == "latency_spike"
    assert signal.metric_name == "p99_latency"
    assert signal.baseline_value == 250
    assert signal.current_value == 1200
    assert signal.unit == "ms"

