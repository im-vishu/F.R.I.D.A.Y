from backend.ai.agent_base import AgentBase
from backend.event_bus import log
import json
import os

class MemoryAgent(AgentBase):
    def __init__(self, event_bus, memfile="memory.jsonl"):
        super().__init__("memory", event_bus)
        self.memfile = memfile
        self.history = []
        self._load_history()
        self.on_event("skills.weather.result", self.log_event)
        self.on_event("skills.wikipedia.result", self.log_event)
        self.on_event("skills.joke.result", self.log_event)
        self.on_event("skills.reminder.result", self.log_event)
        self.on_event("skills.calculator.result", self.log_event)
        self.on_event("skills.quote.result", self.log_event)
        self.on_event("skills.news.result", self.log_event)
        self.on_event("skills.code.result", self.log_event)

    def _load_history(self):
        if os.path.exists(self.memfile):
            with open(self.memfile, "r", encoding="utf-8") as f:
                self.history = [json.loads(line) for line in f]
            log(f"Loaded {len(self.history)} events from {self.memfile}", "info")
        else:
            self.history = []
            log(f"No prior memory found.", "warning")

    def log_event(self, event):
        event_data = event["payload"]
        self.history.append(event_data)
        try:
            with open(self.memfile, "a", encoding="utf-8") as f:
                f.write(json.dumps(event_data, ensure_ascii=False) + "\n")
            log(f"Logged event: {event_data} (Total: {len(self.history)})", "info")
        except Exception as e:
            log(f"Could not write to {self.memfile}: {e}", "error")