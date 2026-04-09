from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from intake_service.config.settings import Settings


def create_session_factory(settings: Settings) -> sessionmaker[Session]:
    engine = create_engine(settings.database.url, future=True)
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)

