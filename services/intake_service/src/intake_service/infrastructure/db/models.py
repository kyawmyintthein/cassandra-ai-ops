from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Float, ForeignKey, Integer, JSON, String, Text, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from intake_service.domain.enums import Classification, InvestigationStatus, QueueMessageStatus, Severity, WorkflowState


def utcnow() -> datetime:
    return datetime.now(UTC)


class Base(DeclarativeBase):
    pass


class RawSignalModel(Base):
    __tablename__ = "raw_signals"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    source: Mapped[str] = mapped_column(String(50))
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    payload: Mapped[dict] = mapped_column(JSON)

    signal: Mapped["SignalModel"] = relationship(back_populates="raw_signal")


class SignalModel(Base):
    __tablename__ = "signals"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    raw_signal_id: Mapped[UUID] = mapped_column(ForeignKey("raw_signals.id"), unique=True)
    source: Mapped[str] = mapped_column(String(50))
    service: Mapped[str | None] = mapped_column(String(100), nullable=True)
    environment: Mapped[str | None] = mapped_column(String(50), nullable=True)
    symptom_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    metric_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    baseline_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    current_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    unit: Mapped[str | None] = mapped_column(String(30), nullable=True)
    detected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    workflow_state: Mapped[str] = mapped_column(String(30), default=WorkflowState.RECEIVED.value)
    classification: Mapped[str | None] = mapped_column(String(30), nullable=True)
    classification_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    assessment_completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    raw_signal: Mapped[RawSignalModel] = relationship(back_populates="signal")
    incident: Mapped["IncidentModel | None"] = relationship(back_populates="signal")
    investigation: Mapped["InvestigationModel | None"] = relationship(back_populates="signal")


class IncidentModel(Base):
    __tablename__ = "incidents"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    signal_id: Mapped[UUID] = mapped_column(ForeignKey("signals.id"), unique=True)
    severity: Mapped[str] = mapped_column(String(20), default=Severity.MEDIUM.value)
    window_start: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    window_end: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    signal: Mapped[SignalModel] = relationship(back_populates="incident")


class InvestigationModel(Base):
    __tablename__ = "investigations"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    signal_id: Mapped[UUID] = mapped_column(ForeignKey("signals.id"), unique=True)
    status: Mapped[str] = mapped_column(String(30), default=InvestigationStatus.REQUESTED.value)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    signal: Mapped[SignalModel] = relationship(back_populates="investigation")


class QueueMessageModel(Base):
    __tablename__ = "queue_messages"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    topic: Mapped[str] = mapped_column(String(100), index=True)
    payload: Mapped[dict] = mapped_column(JSON)
    status: Mapped[str] = mapped_column(String(20), default=QueueMessageStatus.PENDING.value, index=True)
    attempt_count: Mapped[int] = mapped_column(Integer, default=0)
    available_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, index=True)
    locked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)


class ProcessedEventModel(Base):
    __tablename__ = "processed_events"

    event_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    topic: Mapped[str] = mapped_column(String(100))
    processed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
