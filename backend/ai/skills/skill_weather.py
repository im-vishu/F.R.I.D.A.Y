from backend.ai.agent_base import AgentBase

class WeatherSkill(AgentBase):
    def __init__(self, event_bus):
        super().__init__("weather_skill", event_bus)
        self.on_event("planner.invoke.skill", self.handle_skill_request)

    def handle_skill_request(self, event):
        skill = event["payload"].get("skill")
        entities = event["payload"].get("entities", {})
        if skill == "weather":
            location = entities.get("location", "your location")
            # Demo: fake forecast
            result = f"The weather in {location.title()} is sunny and pleasant."
            print(f"[SkillWeather] Responding for: {location}")
            self.publish("skills.weather.result", {"result": result})

if __name__ == "__main__":
    from backend.event_bus import EventBus
    bus = EventBus()
    agent = WeatherSkill(bus)
    bus.run_forever()