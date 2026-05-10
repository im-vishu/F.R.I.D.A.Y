from pydantic import BaseModel, Field
from typing import Any


class OrchestratorRequest(BaseModel):
    message: str = Field(..., min_length=1)
    user_id: str | None = None
    session_id: str | None = None
    context: dict[str, Any] | None = None


class OrchestratorResponse(BaseModel):
    success: bool
    provider: str
    agent: str
    input: str
    response: str
    metadata: dict[str, Any]