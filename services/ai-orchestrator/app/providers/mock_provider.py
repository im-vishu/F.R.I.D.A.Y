from app.prompts.system_prompt import FRIDAY_SYSTEM_PROMPT


class MockProvider:
    name = "mock"

    async def generate(self, message: str, context: dict | None = None) -> str:
        memories = []
        tool_result = None
        agent = None

        if context:
            memories = context.get("memories", [])
            tool_result = context.get("tool_result")
            agent = context.get("agent")

        memory_text = ""

        if memories:
            memory_text = "\nRelevant memories:\n"
            for index, memory in enumerate(memories, start=1):
                memory_text += f"{index}. {memory.get('text')}\n"

        tool_text = ""

        if tool_result:
            tool_text = (
                "\nTool execution result:\n"
                f"Tool: {tool_result.get('tool_name')}\n"
                f"Result: {tool_result.get('result')}\n"
            )

        agent_text = ""

        if agent:
            agent_text = (
                "\nSelected agent:\n"
                f"Agent: {agent.get('name')}\n"
                f"Role: {agent.get('role')}\n"
            )

        return (
            "F.R.I.D.A.Y mock intelligence online.\n\n"
            f"System mode: {FRIDAY_SYSTEM_PROMPT.strip().splitlines()[0]}\n"
            f"{agent_text}"
            f"{memory_text}"
            f"{tool_text}"
            f"User request: {message}\n\n"
            "Agent-aware response: I selected the most relevant specialist agent, "
            "reviewed memory, executed safe tools if needed, and prepared a coordinated response."
        )