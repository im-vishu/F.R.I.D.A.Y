from app.tools.calculator_tool import run_calculator
from app.tools.system_tool import run_system_info


TOOL_REGISTRY = {
    "calculator": {
        "name": "calculator",
        "description": "Safely evaluates basic math expressions.",
        "permission": "basic",
        "handler": run_calculator,
        "input_schema": {
            "expression": "string",
        },
    },
    "system_info": {
        "name": "system_info",
        "description": "Returns current orchestrator system status.",
        "permission": "basic",
        "handler": run_system_info,
        "input_schema": {},
    },
}


def list_tools():
    tools = []

    for tool in TOOL_REGISTRY.values():
        tools.append(
            {
                "name": tool["name"],
                "description": tool["description"],
                "permission": tool["permission"],
                "input_schema": tool["input_schema"],
            }
        )

    return tools


def get_tool(tool_name: str):
    return TOOL_REGISTRY.get(tool_name)