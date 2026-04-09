from __future__ import annotations

from datetime import UTC, datetime, timedelta

from intake_service.domain.contracts import CanonicalSignal, IncidentProjection
from intake_service.domain.enums import Severity


def derive_severity(signal: CanonicalSignal) -> Severity:
    if signal.current_value is None:
        return Severity.MEDIUM
    if signal.baseline_value in (None, 0):
        return Severity.HIGH

    change_ratio = abs(signal.current_value - signal.baseline_value) / abs(signal.baseline_value)
    if change_ratio >= 2:
        return Severity.CRITICAL
    if change_ratio >= 1:
        return Severity.HIGH
    if change_ratio >= 0.5:
        return Severity.MEDIUM
    return Severity.LOW


def derive_incident_projection(signal_id: str, signal: CanonicalSignal) -> IncidentProjection:
    detected_at = signal.detected_at
    window_start = detected_at - timedelta(minutes=30)
    window_end = datetime.now(UTC)
    if window_end < detected_at:
        window_end = detected_at

    return IncidentProjection(
        signal_id=signal_id,
        severity=derive_severity(signal),
        window_start=window_start,
        window_end=window_end,
    )

