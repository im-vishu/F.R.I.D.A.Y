from backend.ai.agent_base import AgentBase
import re

class NLUAgent(AgentBase):
    def __init__(self, event_bus):
        super().__init__("nlu", event_bus)
        self.on_event("stt.result", self.handle_stt)

    def handle_stt(self, event):
        text = event["payload"]["text"].strip().lower()
        print(f"[NLU] Received: {text}")
        # Weather intent
        if "weather" in text:
            location_match = re.search(r'(weather\s+in\s+([a-zA-Z\s]+))', text)
            location = location_match.group(2).strip() if location_match else "your location"
            self.publish("nlu.result",
                         {"intent": "get_weather", "entities": {"location": location or "your location"}})
        # Wikipedia intent
        elif text.startswith("who is ") or text.startswith("what is ") or text.startswith("tell me about"):
            for phrase in ["who is", "what is", "tell me about"]:
                if text.startswith(phrase):
                    query = text[len(phrase):].strip()
                    break
            self.publish("nlu.result",
                         {"intent": "get_wikipedia", "entities": {"query": query}})
        # Joke intent
        elif "joke" in text and ("tell" in text or "say" in text):
            self.publish("nlu.result", {"intent": "get_joke", "entities": {}})
        # Reminder intent
        elif text.startswith("remind me to"):
            task = text[len("remind me to"):].strip()
            self.publish("nlu.result", {"intent": "set_reminder", "entities": {"task": task}})
        elif text.startswith("remind me that"):
            task = text[len("remind me that"):].strip()
            self.publish("nlu.result", {"intent": "set_reminder", "entities": {"task": task}})
        # Calculator intent
        elif text.startswith("calculate "):
            expr = text[len("calculate "):].strip()
            self.publish("nlu.result", {"intent": "do_calculation", "entities": {"expression": expr}})
        elif text.startswith("what is "):
            math_expr = text[len("what is "):].strip()
            if any(op in math_expr for op in "+-*/") and any(c.isdigit() for c in math_expr):
                self.publish("nlu.result", {"intent": "do_calculation", "entities": {"expression": math_expr}})
        # Quote intent
        elif ("quote" in text and ("tell" in text or "give" in text or "say" in text)) or "inspiration" in text:
            self.publish("nlu.result", {"intent": "get_quote", "entities": {}})
        # News intent
        elif "news" in text:
            topic = None
            words = text.split()
            for i, w in enumerate(words):
                if w == "news" and i > 0:
                    topic = words[i-1]
                    break
            self.publish("nlu.result", {"intent": "get_news", "entities": {"topic": topic}})
        # Code execution intent
        elif "run python code" in text or text.startswith("execute ") or text.startswith("run code"):
            if "run python code" in text:
                code = text.split("run python code", 1)[1].strip(": ")
            elif text.startswith("execute "):
                code = text[len("execute "):].strip()
            elif text.startswith("run code"):
                code = text[len("run code"):].strip(": ")
            else:
                code = ""
            self.publish("nlu.result", {"intent": "run_code", "entities": {"code": code}})

if __name__ == "__main__":
    from backend.event_bus import EventBus
    bus = EventBus()
    agent = NLUAgent(bus)
    bus.run_forever()