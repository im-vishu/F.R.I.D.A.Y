from app.prompts.system_prompt import FRIDAY_SYSTEM_PROMPT


class MockProvider:
    name = "mock"

    async def generate(self, message: str, context: dict | None = None) -> str:
        memories = []

        if context:
            memories = context.get("memories", [])

        memory_text = ""

        if memories:
            memory_text = "\nRelevant memories:\n"
            for index, memory in enumerate(memories, start=1):
                memory_text += f"{index}. {memory.get('text')}\n"

        return (
            "F.R.I.D.A.Y mock intelligence online.\n\n"
            f"System mode: {FRIDAY_SYSTEM_PROMPT.strip().splitlines()[0]}\n"
            f"{memory_text}"
            f"User request: {message}\n\n"
            "Memory-aware response: I reviewed stored context before answering. "
            "In the next phase, this response will be powered by OpenAI/Gemini instead of the mock provider."
        )