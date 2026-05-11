from fastapi import APIRouter
from app.agents.agent_service import agent_service

router = APIRouter(prefix="/agents", tags=["agents"])


@router.get("")
def get_agents():
    return agent_service.list_available_agents()