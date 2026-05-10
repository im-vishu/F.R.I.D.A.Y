from datetime import datetime, timezone

from app.config.settings import settings
from app.providers.mock_provider import MockProvider
from app.schemas.orchestrator_schema import OrchestratorRequest
from app.schemas.memory_schema import StoreMemoryRequest, SearchMemoryRequest
from app.memory.memory_service import memory_service


class OrchestratorService:
    def __init__(self):
        self.provider = self._load_provider()

    def _load_provider(self):
        if settings.DEFAULT_PROVIDER == "mock":
            return MockProvider()

        return MockProvider()

    async def orchestrate(self, payload: OrchestratorRequest):
        user_id = payload.user_id or "anonymous"
        session_id = payload.session_id or "default-session"

        memory_results = memory_service.search_memory(
            SearchMemoryRequest(
                user_id=user_id,
                query=payload.message,
                limit=5,
            )
        )

        memories = memory_results.get("memories", [])

        enhanced_context = {
            **(payload.context or {}),
            "memories": memories,
        }

        response = await self.provider.generate(
            message=payload.message,
            context=enhanced_context,
        )

        memory_service.store_memory(
            StoreMemoryRequest(
                user_id=user_id,
                session_id=session_id,
                text=payload.message,
                metadata={
                    "source": "orchestrator",
                    "type": "user_message",
                    "created_by": "phase-5.1",
                },
            )
        )

        return {
            "success": True,
            "provider": self.provider.name,
            "agent": "coordinator-agent",
            "input": payload.message,
            "response": response,
            "metadata": {
                "user_id": user_id,
                "session_id": session_id,
                "environment": settings.APP_ENV,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "memory_enabled": True,
                "memory_count": len(memories),
                "tools_enabled": False,
                "streaming_enabled": False,
            },
        }


orchestrator_service = OrchestratorService()