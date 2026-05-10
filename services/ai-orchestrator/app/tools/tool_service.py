from datetime import datetime, timezone

from app.schemas.tool_schema import ToolExecuteRequest
from app.tools.registry import get_tool, list_tools


class ToolService:
    def list_available_tools(self):
        return {
            "success": True,
            "tools": list_tools(),
            "count": len(list_tools()),
        }

    def execute_tool(self, payload: ToolExecuteRequest):
        tool = get_tool(payload.tool_name)

        if not tool:
            return {
                "success": False,
                "tool_name": payload.tool_name,
                "result": {
                    "error": "Tool not found",
                },
                "metadata": {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                },
            }

        result = tool["handler"](payload.input)

        return {
            "success": result.get("success", False),
            "tool_name": payload.tool_name,
            "result": result,
            "metadata": {
                "user_id": payload.user_id,
                "session_id": payload.session_id,
                "permission": tool["permission"],
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        }


tool_service = ToolService()