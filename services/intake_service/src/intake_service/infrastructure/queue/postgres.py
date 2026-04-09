from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.orm import Session, sessionmaker

from intake_service.domain.contracts import QueueEvent, QueueMessage
from intake_service.domain.enums import QueueMessageStatus
from intake_service.infrastructure.db.models import QueueMessageModel
from intake_service.infrastructure.queue.base import QueueBackend


class PostgresQueueBackend(QueueBackend):
    def __init__(self, session_factory: sessionmaker[Session], retry_delay_seconds: int = 30) -> None:
        self.session_factory = session_factory
        self.retry_delay_seconds = retry_delay_seconds

    def publish(self, event: QueueEvent) -> None:
        with self.session_factory.begin() as session:
            session.add(
                QueueMessageModel(
                    id=UUID(event.event_id),
                    topic=event.topic,
                    payload=event.payload,
                    status=QueueMessageStatus.PENDING.value,
                    available_at=datetime.now(UTC),
                )
            )

    def consume(self, topic: str, batch_size: int) -> list[QueueMessage]:
        with self.session_factory.begin() as session:
            now = datetime.now(UTC)
            stmt = (
                select(QueueMessageModel)
                .where(
                    QueueMessageModel.topic == topic,
                    or_(
                        QueueMessageModel.status == QueueMessageStatus.PENDING.value,
                        QueueMessageModel.status == QueueMessageStatus.FAILED.value,
                    ),
                    QueueMessageModel.available_at <= now,
                )
                .order_by(QueueMessageModel.available_at.asc())
                .with_for_update(skip_locked=True)
                .limit(batch_size)
            )
            rows = list(session.execute(stmt).scalars())
            messages: list[QueueMessage] = []
            for row in rows:
                row.status = QueueMessageStatus.PROCESSING.value
                row.locked_at = now
                row.attempt_count += 1
                messages.append(
                    QueueMessage(
                        id=row.id,
                        topic=row.topic,
                        payload=row.payload,
                        attempt_count=row.attempt_count,
                    )
                )
            return messages

    def acknowledge(self, message_id: UUID) -> None:
        with self.session_factory.begin() as session:
            message = session.get(QueueMessageModel, message_id)
            if message is None:
                return
            message.status = QueueMessageStatus.COMPLETED.value
            message.locked_at = None

    def retry(self, message_id: UUID, error: str) -> None:
        with self.session_factory.begin() as session:
            message = session.get(QueueMessageModel, message_id)
            if message is None:
                return
            message.status = QueueMessageStatus.FAILED.value
            message.locked_at = None
            message.last_error = error
            message.available_at = datetime.now(UTC) + timedelta(seconds=self.retry_delay_seconds)
