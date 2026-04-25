from backend.event_bus import EventBus
from backend.ai.nlu_agent import NLUAgent
from backend.ai.planner_agent import PlannerAgent
from backend.ai.skills.skill_weather import WeatherSkill
from backend.ai.skills.skill_wikipedia import WikipediaSkill
from backend.ai.skills.skill_joke import JokeSkill
from backend.ai.skills.skill_reminder import ReminderSkill
from backend.ai.skills.skill_calculator import CalculatorSkill
from backend.ai.skills.skill_quote import QuoteSkill
from backend.ai.skills.skill_news import NewsSkill
from backend.ai.skills.skill_code import CodeSkill
from backend.ai.tts_agent import TTSAgent
from backend.ai.memory_agent import MemoryAgent

bus = EventBus()
nlu = NLUAgent(bus)
planner = PlannerAgent(bus)
weather = WeatherSkill(bus)
wikipedia = WikipediaSkill(bus)
joke = JokeSkill(bus)
reminder = ReminderSkill(bus)
calculator = CalculatorSkill(bus)
quote = QuoteSkill(bus)
news = NewsSkill(bus)
code = CodeSkill(bus)
tts = TTSAgent(bus)
mem = MemoryAgent(bus)

# Test: "run python code: print(42 * 7)"
bus.publish_event("stt.result", {
    "origin": "stt",
    "type": "stt.result",
    "payload": {"text": "run python code: print(42 * 7)"},
    "target": "broadcast"
})

bus.run_forever()