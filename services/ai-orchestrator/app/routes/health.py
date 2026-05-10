from datetime import datetime, timezone
from fastapi import APIRouter

from app.config.settings import settings
from app.memory.qdrant_client import ensure_memory_collection
from app.tools.registry import list_tools

router = APIRouter()


@router.get("/health")
def health():
    qdrant_status = "connected"

    try:
        ensure_memory_collection()
    except Exception:
        qdrant_status = "disconnected"

    return {
        "success": True,
        "service": settings.APP_NAME,
        "status": "healthy" if qdrant_status == "connected" else "degraded",
        "environment": settings.APP_ENV,
        "modules": {
            "orchestrator": "online",
            "provider": settings.DEFAULT_PROVIDER,
            "memory": qdrant_status,
            "tools": "enabled",
            "tool_count": len(list_tools()),
            "streaming": "pending",
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }