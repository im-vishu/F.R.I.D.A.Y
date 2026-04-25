from backend.ai.agent_base import AgentBase
import random

class QuoteSkill(AgentBase):
    def __init__(self, event_bus):
        super().__init__("quote_skill", event_bus)
        self.on_event("planner.invoke.skill", self.handle_skill_request)
        self.quotes = [
            "The best way to get started is to quit talking and begin doing. — Walt Disney",
            "Don't watch the clock; do what it does. Keep going. — Sam Levenson",
            "Success is not final, failure is not fatal: it is the courage to continue that counts. — Winston Churchill",
            "Your time is limited, so don't waste it living someone else's life. — Steve Jobs",
            "The only way to do great work is to love what you do. — Steve Jobs",
            "You only live once, but if you do it right, once is enough. — Mae West",
            "The best revenge is massive success. — Frank Sinatra"
        ]

    def handle_skill_request(self, event):
        skill = event["payload"].get("skill")
        if skill == "quote":
            quote = random.choice(self.quotes)
            print(f"[SkillQuote] Sharing a quote.")
            self.publish("skills.quote.result", {"result": quote})

if __name__ == "__main__":
    from backend.event_bus import EventBus
    bus = EventBus()
    skill = QuoteSkill(bus)
    bus.run_forever()