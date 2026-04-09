from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20260408_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "raw_signals",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("source", sa.String(length=50), nullable=False),
        sa.Column("received_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
    )

    op.create_table(
        "signals",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("raw_signal_id", sa.Uuid(as_uuid=True), sa.ForeignKey("raw_signals.id"), nullable=False, unique=True),
        sa.Column("source", sa.String(length=50), nullable=False),
        sa.Column("service", sa.String(length=100), nullable=True),
        sa.Column("environment", sa.String(length=50), nullable=True),
        sa.Column("symptom_type", sa.String(length=50), nullable=True),
        sa.Column("metric_name", sa.String(length=100), nullable=True),
        sa.Column("baseline_value", sa.Float(), nullable=True),
        sa.Column("current_value", sa.Float(), nullable=True),
        sa.Column("unit", sa.String(length=30), nullable=True),
        sa.Column("detected_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("workflow_state", sa.String(length=30), nullable=False),
        sa.Column("classification", sa.String(length=30), nullable=True),
        sa.Column("classification_reason", sa.Text(), nullable=True),
        sa.Column("assessment_completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "incidents",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("signal_id", sa.Uuid(as_uuid=True), sa.ForeignKey("signals.id"), nullable=False, unique=True),
        sa.Column("severity", sa.String(length=20), nullable=False),
        sa.Column("window_start", sa.DateTime(timezone=True), nullable=False),
        sa.Column("window_end", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "investigations",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("signal_id", sa.Uuid(as_uuid=True), sa.ForeignKey("signals.id"), nullable=False, unique=True),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "queue_messages",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("topic", sa.String(length=100), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("attempt_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("available_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("locked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_error", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_queue_messages_topic_status_available_at", "queue_messages", ["topic", "status", "available_at"])

    op.create_table(
        "processed_events",
        sa.Column("event_id", sa.String(length=100), primary_key=True),
        sa.Column("topic", sa.String(length=100), nullable=False),
        sa.Column("processed_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("processed_events")
    op.drop_index("ix_queue_messages_topic_status_available_at", table_name="queue_messages")
    op.drop_table("queue_messages")
    op.drop_table("investigations")
    op.drop_table("incidents")
    op.drop_table("signals")
    op.drop_table("raw_signals")
