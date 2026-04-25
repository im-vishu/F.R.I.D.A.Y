from backend.ai.agent_base import AgentBase
import random

class JokeSkill(AgentBase):
    def __init__(self, event_bus):
        super().__init__("joke_skill", event_bus)
        self.on_event("planner.invoke.skill", self.handle_skill_request)
        self.jokes = [
            "Why did the computer show up at work late? Because it had a hard drive!",
            "Why do programmers prefer dark mode? Because light attracts bugs.",
            "Why was the math book sad? Because it had too many problems.",
            "What do you call 8 hobbits? A hobbyte.",
            "Why did the scarecrow win an award? Because he was outstanding in his field."
        ]

    def handle_skill_request(self, event):
        skill = event["payload"].get("skill")
        if skill == "joke":
            joke = random.choice(self.jokes)
            print(f"[SkillJoke] Telling a joke.")
            self.publish("skills.joke.result", {"result": joke})

if __name__ == "__main__":
    from backend.event_bus import EventBus
    bus = EventBus()
    skill = JokeSkill(bus)
    bus.run_forever()