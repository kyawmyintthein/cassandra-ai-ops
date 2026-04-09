from __future__ import annotations

from collections.abc import Generator
from functools import lru_cache

from fastapi import Depends
from sqlalchemy.orm import Session, sessionmaker

from intake_service.application.assessment_service import AssessmentService
from intake_service.application.intake_service import IntakeService
from intake_service.config.settings import Settings, load_settings
from intake_service.infrastructure.db.session import create_session_factory
from intake_service.infrastructure.queue.base import QueueBackend
from intake_service.infrastructure.queue.postgres import PostgresQueueBackend


@lru_cache
def get_settings() -> Settings:
    return load_settings()


@lru_cache
def get_session_factory() -> sessionmaker[Session]:
    return create_session_factory(get_settings())


@lru_cache
def get_queue_backend() -> QueueBackend:
    return PostgresQueueBackend(get_session_factory())


def get_db_session() -> Generator[Session, None, None]:
    session = get_session_factory()()
    try:
        yield session
    finally:
        session.close()


def get_intake_service(
    session: Session = Depends(get_db_session),
    queue_backend: QueueBackend = Depends(get_queue_backend),
) -> IntakeService:
    return IntakeService(session, queue_backend)


def get_assessment_service(
    session: Session = Depends(get_db_session),
    queue_backend: QueueBackend = Depends(get_queue_backend),
) -> AssessmentService:
    return AssessmentService(session, queue_backend)
