from pydantic import BaseModel, Field
from typing import Any


class ToolExecuteRequest(BaseModel):
    tool_name: str = Field(..., min_length=1)
    input: dict[str, Any] = {}
    user_id: str | None = None
    session_id: str | None = None


class ToolExecuteResponse(BaseModel):
    success: bool
    tool_name: str
    result: dict[str, Any]
    metadata: dict[str, Any]