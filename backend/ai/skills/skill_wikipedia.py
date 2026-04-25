from backend.ai.agent_base import AgentBase
import requests

class WikipediaSkill(AgentBase):
    def __init__(self, event_bus):
        super().__init__("wikipedia_skill", event_bus)
        self.on_event("planner.invoke.skill", self.handle_skill_request)

    def handle_skill_request(self, event):
        skill = event["payload"].get("skill")
        entities = event["payload"].get("entities", {})
        if skill == "wikipedia":
            query = entities.get("query", "")
            result = self.search_wikipedia(query)
            print(f"[SkillWikipedia] Responding for: {query}")
            self.publish("skills.wikipedia.result", {"result": result})

    def search_wikipedia(self, query):
        if not query:
            return "I need to know what you want to know about!"
        api = "https://en.wikipedia.org/api/rest_v1/page/summary/" + query.replace(" ", "_")
        try:
            resp = requests.get(api)
            if resp.status_code == 200:
                data = resp.json()
                return data.get("extract", "Sorry, I couldn't find information.")
            else:
                return "I couldn't find anything interesting on Wikipedia."
        except Exception:
            return "Could not connect to Wikipedia for that info."

if __name__ == "__main__":
    from backend.event_bus import EventBus
    bus = EventBus()
    skill = WikipediaSkill(bus)
    bus.run_forever()