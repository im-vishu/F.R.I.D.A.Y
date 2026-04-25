from backend.ai.agent_base import AgentBase

class MemoryAgent(AgentBase):
    def __init__(self, event_bus):
        super().__init__("memory", event_bus)
        self.history = []
        self.on_event("skills.weather.result", self.log_event)
        self.on_event("skills.wikipedia.result", self.log_event)
        self.on_event("skills.joke.result", self.log_event)
        self.on_event("skills.reminder.result", self.log_event)
        self.on_event("skills.calculator.result", self.log_event)
        self.on_event("skills.quote.result", self.log_event)
        self.on_event("skills.news.result", self.log_event)
        self.on_event("skills.code.result", self.log_event)

    def log_event(self, event):
        self.history.append(event["payload"])
        print(f"[Memory] Logged: {event['payload']} (Total: {len(self.history)})")

if __name__ == "__main__":
    from backend.event_bus import EventBus
    bus = EventBus()
    agent = MemoryAgent(bus)
    bus.run_forever()