from backend.ai.agent_base import AgentBase
import pyttsx3

class TTSAgent(AgentBase):
    def __init__(self, event_bus):
        super().__init__("tts", event_bus)
        self.engine = pyttsx3.init()
        self.on_event("skills.weather.result", self.speak_response)
        self.on_event("skills.wikipedia.result", self.speak_response)
        self.on_event("skills.joke.result", self.speak_response)
        self.on_event("skills.reminder.result", self.speak_response)
        self.on_event("skills.calculator.result", self.speak_response)
        self.on_event("skills.quote.result", self.speak_response)
        self.on_event("skills.news.result", self.speak_response)
        self.on_event("skills.code.result", self.speak_response)

    def speak_response(self, event):
        response = event["payload"].get("result") or event["payload"].get("text")
        if response:
            print(f"[TTS] Speaking: {response}")
            self.engine.say(response)
            self.engine.runAndWait()

if __name__ == "__main__":
    from backend.event_bus import EventBus
    bus = EventBus()
    agent = TTSAgent(bus)
    bus.run_forever()