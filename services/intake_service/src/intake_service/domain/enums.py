from __future__ import annotations

from enum import StrEnum


class SignalSource(StrEnum):
    USER = "user"
    OBSERVABILITY_WEBHOOK = "observability_webhook"
    ANOMALY_DETECTION = "anomaly_detection"


class WorkflowState(StrEnum):
    RECEIVED = "received"
    ASSESSMENT_REQUESTED = "assessment_requested"
    ALERT = "alert"
    INCIDENT = "incident"
    INVESTIGATION_REQUESTED = "investigation_requested"


class Classification(StrEnum):
    ALERT = "alert"
    INCIDENT = "incident"


class Severity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class InvestigationStatus(StrEnum):
    REQUESTED = "requested"


class QueueMessageStatus(StrEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    FAILED = "failed"
    COMPLETED = "completed"

