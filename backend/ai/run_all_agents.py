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
from backend.ai.gui_agent import GUIAgent
from backend.ai.speech_agent import SpeechAgent

bus = EventBus()

# Core agents
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

# GUI Agent (text/chat window)
gui = GUIAgent(bus)
gui.start_mainloop()

# Speech Agent (microphone input; requires Vosk and model)
speech = SpeechAgent(bus)            # You can comment this out if you want text-only
speech.start_listen_thread()         # Comment out to disable live STT

print("[F.R.I.D.A.Y] System ready. Use GUI, type, or speak your requests!")

bus.run_forever()