from backend.ai.agent_base import AgentBase

class PlannerAgent(AgentBase):
    def __init__(self, event_bus):
        super().__init__("planner", event_bus)
        self.on_event("nlu.intent", self.handle_intent)

    def handle_intent(self, event):
        intent = event["payload"].get("intent", "")
        entities = event["payload"].get("entities", {})
        # Example: For get_weather, call skill agent
        if intent == "get_weather":
            plan = {"skill": "skill_weather", "args": entities}
            self.publish("planner.plan", plan, target="skill_weather")

if __name__ == "__main__":
    from backend.event_bus import EventBus
    bus = EventBus()
    agent = PlannerAgent(bus)
    bus.run_forever()