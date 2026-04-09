from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os
from typing import Any

import yaml


DEFAULT_CONFIG_PATH = Path(__file__).resolve().parents[3] / "config" / "application.yaml"


@dataclass(frozen=True)
class ServiceConfig:
    name: str
    environment: str


@dataclass(frozen=True)
class ApiConfig:
    host: str
    port: int


@dataclass(frozen=True)
class DatabaseConfig:
    url: str


@dataclass(frozen=True)
class QueueConfig:
    backend: str
    poll_interval_seconds: int
    batch_size: int


@dataclass(frozen=True)
class Settings:
    service: ServiceConfig
    api: ApiConfig
    database: DatabaseConfig
    queue: QueueConfig


def expand_env_vars(value: Any) -> Any:
    if isinstance(value, str):
        return os.path.expandvars(value)
    if isinstance(value, dict):
        return {key: expand_env_vars(nested_value) for key, nested_value in value.items()}
    if isinstance(value, list):
        return [expand_env_vars(item) for item in value]
    return value


def load_settings(config_path: str | None = None) -> Settings:
    path = Path(config_path or os.getenv("INTAKE_CONFIG_PATH", DEFAULT_CONFIG_PATH))
    raw = expand_env_vars(yaml.safe_load(path.read_text()))
    return Settings(
        service=ServiceConfig(**raw["service"]),
        api=ApiConfig(**raw["api"]),
        database=DatabaseConfig(**raw["database"]),
        queue=QueueConfig(**raw["queue"]),
    )
