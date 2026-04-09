from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from intake_service.domain.enums import Classification, SignalSource, Severity, WorkflowState


class SignalIngestRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    source: SignalSource
    detected_at: datetime
    service: str | None = None
    environment: str | None = None
    symptom_type: str | None = None
    metric_name: str | None = None
    baseline_value: float | None = None
    current_value: float | None = None
    unit: str | None = None
    payload: dict[str, Any] = Field(default_factory=dict)


class SignalIngestResponse(BaseModel):
    signal_id: UUID
    raw_signal_id: UUID
    workflow_state: WorkflowState


class AssessmentResultRequest(BaseModel):
    event_id: str = Field(min_length=1, max_length=100)
    signal_id: UUID
    classification: Classification
    reason: str | None = None
