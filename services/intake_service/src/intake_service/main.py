from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from intake_service.api.routes import router
from intake_service.api.dependencies import get_settings


settings = get_settings()

app = FastAPI(
    title="Cassandra AI Ops Intake Service",
    version="0.1.0",
    description="Receives signals, normalizes them, persists them, and drives intake workflow events.",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    swagger_ui_parameters={
        "displayRequestDuration": True,
        "docExpansion": "list",
    },
)
app.include_router(router)


@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    return RedirectResponse(url="/docs", status_code=307)


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {
        "status": "ok",
        "service": settings.service.name,
        "environment": settings.service.environment,
    }
