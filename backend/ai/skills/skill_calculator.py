from backend.ai.agent_base import AgentBase

class CalculatorSkill(AgentBase):
    def __init__(self, event_bus):
        super().__init__("calculator_skill", event_bus)
        self.on_event("planner.invoke.skill", self.handle_skill_request)

    def handle_skill_request(self, event):
        skill = event["payload"].get("skill")
        entities = event["payload"].get("entities", {})
        if skill == "calculator":
            expr = entities.get("expression")
            if not expr:
                result = "Please specify a calculation."
            else:
                try:
                    # Security: Only allow digits, +, -, *, /, (, ), . and spaces for evaluation
                    if not all(c in "0123456789.+-*/() " for c in expr):
                        raise ValueError
                    answer = eval(expr)
                    result = f"The answer is {answer}."
                except Exception:
                    result = "Sorry, I couldn't calculate that."
            print(f"[SkillCalculator] {expr} = {result}")
            self.publish("skills.calculator.result", {"result": result})

if __name__ == "__main__":
    from backend.event_bus import EventBus
    bus = EventBus()
    skill = CalculatorSkill(bus)
    bus.run_forever()