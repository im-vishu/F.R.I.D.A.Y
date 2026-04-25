from backend.ai.agent_base import AgentBase

class WeatherSkill(AgentBase):
    def __init__(self, event_bus):
        super().__init__("skill_weather", event_bus)
        self.on_event("planner.plan", self.handle_plan)

    def handle_plan(self, event):
        args = event["payload"].get("args", {})
        # Call weather API or dummy response
        result = {"result": f"The weather in {args.get('location', 'your city')} is 20°C and sunny."}
        self.publish("skills.weather.result", result, target=event["origin"])

if __name__ == "__main__":
    from backend.event_bus import EventBus
    bus = EventBus()
    skill = WeatherSkill(bus)
    bus.run_forever()