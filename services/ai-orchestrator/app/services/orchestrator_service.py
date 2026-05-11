from datetime import datetime, timezone

from app.config.settings import settings
from app.providers.mock_provider import MockProvider
from app.schemas.orchestrator_schema import OrchestratorRequest
from app.schemas.memory_schema import StoreMemoryRequest, SearchMemoryRequest
from app.schemas.tool_schema import ToolExecuteRequest
from app.memory.memory_service import memory_service
from app.tools.tool_service import tool_service
from app.agents.agent_service import agent_service


class OrchestratorService:
    def __init__(self):
        self.provider = self._load_provider()

    def _load_provider(self):
        if settings.DEFAULT_PROVIDER == "mock":
            return MockProvider()

        return MockProvider()

    def _detect_tool(self, message: str):
        lower_message = message.lower().strip()

        calculator_keywords = ["calculate", "calculator", "solve", "math"]
        system_keywords = [
            "system info",
            "system status",
            "orchestrator status",
            "server status",
        ]

        if any(keyword in lower_message for keyword in calculator_keywords):
            expression = (
                lower_message
                .replace("calculate", "")
                .replace("calculator", "")
                .replace("solve", "")
                .replace("math", "")
                .strip()
            )

            return {
                "tool_name": "calculator",
                "input": {
                    "expression": expression,
                },
            }

        if any(keyword in lower_message for keyword in system_keywords):
            return {
                "tool_name": "system_info",
                "input": {},
            }

        return None

    async def orchestrate(self, payload: OrchestratorRequest):
        user_id = payload.user_id or "anonymous"
        session_id = payload.session_id or "default-session"

        selected_agent = agent_service.select_agent(payload.message)
        agent = selected_agent["agent"]

        memory_results = memory_service.search_memory(
            SearchMemoryRequest(
                user_id=user_id,
                query=payload.message,
                limit=5,
            )
        )

        memories = memory_results.get("memories", [])

        tool_result = None
        detected_tool = self._detect_tool(payload.message)

        if detected_tool:
            tool_result = tool_service.execute_tool(
                ToolExecuteRequest(
                    tool_name=detected_tool["tool_name"],
                    input=detected_tool["input"],
                    user_id=user_id,
                    session_id=session_id,
                )
            )

        enhanced_context = {
            **(payload.context or {}),
            "agent": agent,
            "memories": memories,
            "tool_result": tool_result,
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
                    "created_by": "phase-7",
                    "agent": agent.get("name"),
                    "tool_used": tool_result.get("tool_name") if tool_result else None,
                },
            )
        )

        return {
            "success": True,
            "provider": self.provider.name,
            "agent": agent.get("name"),
            "agent_role": agent.get("role"),
            "agent_score": selected_agent["score"],
            "input": payload.message,
            "response": response,
            "metadata": {
                "user_id": user_id,
                "session_id": session_id,
                "environment": settings.APP_ENV,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "memory_enabled": True,
                "memory_count": len(memories),
                "tools_enabled": True,
                "tool_executed": tool_result.get("tool_name") if tool_result else None,
                "multi_agent_enabled": True,
                "selected_agent": agent.get("name"),
                "streaming_enabled": False,
            },
        }


orchestrator_service = OrchestratorService()