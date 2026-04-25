from backend.ai.agent_base import AgentBase
import io
import contextlib

class CodeSkill(AgentBase):
    def __init__(self, event_bus):
        super().__init__("code_skill", event_bus)
        self.on_event("planner.invoke.skill", self.handle_skill_request)

    def handle_skill_request(self, event):
        skill = event["payload"].get("skill")
        entities = event["payload"].get("entities", {})
        if skill == "code":
            code = entities.get("code")
            if not code:
                result = "Please provide the code to execute."
            else:
                result = self.run_python_code(code)
            print(f"[SkillCode] Executed code. Result: {result}")
            self.publish("skills.code.result", {"result": result})

    def run_python_code(self, code):
        # For safety, disable builtins except a minimal list
        safe_builtins = {"print": print, "range": range, "len": len, "str": str, "int": int, "float": float, "bool": bool, "list": list, "dict": dict, "set": set, "min": min, "max": max, "sum": sum}
        output = io.StringIO()
        try:
            with contextlib.redirect_stdout(output):
                exec(code, {"__builtins__": safe_builtins}, {})
            return output.getvalue().strip() or "[Code ran successfully with no output.]"
        except Exception as e:
            return f"Error during code execution: {e}"

if __name__ == "__main__":
    from backend.event_bus import EventBus
    bus = EventBus()
    skill = CodeSkill(bus)
    bus.run_forever()