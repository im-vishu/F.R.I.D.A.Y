from backend.ai.agent_base import AgentBase

class PlannerAgent(AgentBase):
    def __init__(self, event_bus):
        super().__init__("planner", event_bus)
        self.on_event("nlu.result", self.handle_nlu)

    def handle_nlu(self, event):
        intent = event["payload"].get("intent")
        entities = event["payload"].get("entities", {})
        print(f"[Planner] Intent: {intent}, Entities: {entities}")
        if intent == "get_weather":
            self.publish("planner.invoke.skill",
                         {"skill": "weather", "entities": entities, "original_event": event})
        elif intent == "get_wikipedia":
            self.publish("planner.invoke.skill",
                         {"skill": "wikipedia", "entities": entities, "original_event": event})
        elif intent == "get_joke":
            self.publish("planner.invoke.skill",
                         {"skill": "joke", "entities": entities, "original_event": event})
        elif intent == "set_reminder":
            self.publish("planner.invoke.skill",
                         {"skill": "reminder", "entities": entities, "original_event": event})
        elif intent == "do_calculation":
            self.publish("planner.invoke.skill",
                         {"skill": "calculator", "entities": entities, "original_event": event})
        elif intent == "get_quote":
            self.publish("planner.invoke.skill",
                         {"skill": "quote", "entities": entities, "original_event": event})
        elif intent == "get_news":
            self.publish("planner.invoke.skill",
                         {"skill": "news", "entities": entities, "original_event": event})
        elif intent == "run_code":
            self.publish("planner.invoke.skill",
                         {"skill": "code", "entities": entities, "original_event": event})

if __name__ == "__main__":
    from backend.event_bus import EventBus
    bus = EventBus()
    agent = PlannerAgent(bus)
    bus.run_forever()