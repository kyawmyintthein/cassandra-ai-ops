from __future__ import annotations

from fastapi import APIRouter, Depends, status

from intake_service.api.dependencies import get_intake_service
from intake_service.api.schemas import SignalIngestRequest, SignalIngestResponse
from intake_service.application.intake_service import IntakeService


router = APIRouter()


@router.post("/signals", response_model=SignalIngestResponse, status_code=status.HTTP_202_ACCEPTED)
def create_signal(
    request: SignalIngestRequest,
    service: IntakeService = Depends(get_intake_service),
) -> SignalIngestResponse:
    return service.ingest_signal(request)
