from datetime import datetime, timezone
from app.config.settings import settings


def run_system_info(input_data: dict):
    return {
        "success": True,
        "system": "F.R.I.D.A.Y AI Orchestrator",
        "environment": settings.APP_ENV,
        "provider": settings.DEFAULT_PROVIDER,
        "memory": "enabled",
        "tools": "enabled",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }