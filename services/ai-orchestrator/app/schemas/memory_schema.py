from pydantic import BaseModel, Field
from typing import Any


class StoreMemoryRequest(BaseModel):
    user_id: str = Field(..., min_length=1)
    session_id: str | None = None
    text: str = Field(..., min_length=1)
    metadata: dict[str, Any] | None = None


class SearchMemoryRequest(BaseModel):
    user_id: str = Field(..., min_length=1)
    query: str = Field(..., min_length=1)
    limit: int = 5