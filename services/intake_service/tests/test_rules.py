from __future__ import annotations

from datetime import UTC, datetime

from intake_service.domain.contracts import CanonicalSignal
from intake_service.domain.enums import Severity, SignalSource
from intake_service.domain.rules import derive_incident_projection, derive_severity


def test_derive_severity_marks_large_regression_critical() -> None:
    signal = CanonicalSignal(
        source=SignalSource.OBSERVABILITY_WEBHOOK,
        service="api",
        environment="prod",
        symptom_type="error_rate",
        metric_name="5xx_rate",
        baseline_value=2.0,
        current_value=8.5,
        unit="percent",
        detected_at=datetime(2026, 4, 8, 1, 0, tzinfo=UTC),
    )

    assert derive_severity(signal) == Severity.CRITICAL


def test_projection_uses_detected_at_minus_thirty_minutes() -> None:
    detected_at = datetime(2026, 4, 8, 2, 0, tzinfo=UTC)
    signal = CanonicalSignal(
        source=SignalSource.USER,
        service="orders",
        environment="prod",
        symptom_type="availability",
        metric_name="uptime",
        baseline_value=100.0,
        current_value=40.0,
        unit="percent",
        detected_at=detected_at,
    )

    projection = derive_incident_projection("signal-1", signal)

    assert projection.window_start == datetime(2026, 4, 8, 1, 30, tzinfo=UTC)
    assert projection.window_end >= detected_at

