from fastapi import APIRouter
from app.schemas.orchestrator_schema import (
    OrchestratorRequest,
    OrchestratorResponse,
)
from app.services.orchestrator_service import orchestrator_service

router = APIRouter(prefix="/orchestrator", tags=["orchestrator"])


@router.post("/run", response_model=OrchestratorResponse)
async def run_orchestrator(payload: OrchestratorRequest):
    return await orchestrator_service.orchestrate(payload)