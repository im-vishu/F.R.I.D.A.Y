from backend.ai.agent_base import AgentBase
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env at project root
load_dotenv()

class NewsSkill(AgentBase):
    def __init__(self, event_bus):
        super().__init__("news_skill", event_bus)
        self.on_event("planner.invoke.skill", self.handle_skill_request)
        # Load API KEY from environment
        self.API_KEY = os.getenv("NEWSAPI_KEY", "YOUR_NEWSAPI_KEY")

    def handle_skill_request(self, event):
        skill = event["payload"].get("skill")
        entities = event["payload"].get("entities", {})
        if skill == "news":
            topic = entities.get("topic") or "latest"
            result = self.get_news(topic)
            print(f"[SkillNews] News for: {topic}")
            self.publish("skills.news.result", {"result": result})

    def get_news(self, topic):
        if not self.API_KEY or self.API_KEY == "YOUR_NEWSAPI_KEY":
            # Fallback: no real API key, return demo news.
            return "Today's top headline: 'Open-source AI is taking over the world!'"
        try:
            url = f"https://newsapi.org/v2/top-headlines?country=us&q={topic}&apiKey={self.API_KEY}"
            r = requests.get(url)
            data = r.json()
            if "articles" in data and data["articles"]:
                article = data["articles"][0]
                return f"{article['title']} — {article.get('description', '')}"
            else:
                return f"Sorry, I couldn't find news about {topic}."
        except Exception as e:
            print(f"[SkillNews] Exception: {e}")
            return "Sorry, I was unable to fetch the news headline."

if __name__ == "__main__":
    from backend.event_bus import EventBus
    bus = EventBus()
    skill = NewsSkill(bus)
    bus.run_forever()