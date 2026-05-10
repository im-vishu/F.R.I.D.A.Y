from fastapi import APIRouter

from app.schemas.tool_schema import ToolExecuteRequest, ToolExecuteResponse
from app.tools.tool_service import tool_service

router = APIRouter(prefix="/tools", tags=["tools"])


@router.get("")
def get_tools():
    return tool_service.list_available_tools()


@router.post("/execute", response_model=ToolExecuteResponse)
def execute_tool(payload: ToolExecuteRequest):
    return tool_service.execute_tool(payload)