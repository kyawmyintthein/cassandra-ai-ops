from __future__ import annotations

from collections.abc import Callable

from pydantic import ValidationError
from sqlalchemy.orm import Session, sessionmaker

from intake_service.api.schemas import AssessmentResultRequest
from intake_service.application.assessment_service import AssessmentService
from intake_service.infrastructure.queue.base import QueueBackend


class AssessmentResultHandler:
    def __init__(
        self,
        session_factory: sessionmaker[Session],
        queue_backend: QueueBackend,
        assessment_service_factory: Callable[[Session], AssessmentService],
        batch_size: int,
    ) -> None:
        self.session_factory = session_factory
        self.queue_backend = queue_backend
        self.assessment_service_factory = assessment_service_factory
        self.batch_size = batch_size

    def poll_once(self) -> int:
        messages = self.queue_backend.consume("signal.assessed", self.batch_size)
        for message in messages:
            try:
                payload = AssessmentResultRequest.model_validate(message.payload)
                with self.session_factory() as session:
                    service = self.assessment_service_factory(session)
                    service.process_result(payload)
                self.queue_backend.acknowledge(message.id)
            except (ValidationError, ValueError) as exc:
                self.queue_backend.retry(message.id, str(exc))
        return len(messages)
