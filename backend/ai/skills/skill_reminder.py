from backend.ai.agent_base import AgentBase
import time

class ReminderSkill(AgentBase):
    def __init__(self, event_bus):
        super().__init__("reminder_skill", event_bus)
        self.on_event("planner.invoke.skill", self.handle_skill_request)
        self.reminders = []  # Store reminders in memory for demo

    def handle_skill_request(self, event):
        skill = event["payload"].get("skill")
        entities = event["payload"].get("entities", {})
        if skill == "reminder":
            task = entities.get("task", None)
            if not task:
                response = "What should I remind you?"
            else:
                self.reminders.append({"task": task, "timestamp": time.time()})
                response = f"Okay, I'll remind you to {task}."
            print(f"[SkillReminder] Reminder set: {task}")
            self.publish("skills.reminder.result", {"result": response})

if __name__ == "__main__":
    from backend.event_bus import EventBus
    bus = EventBus()
    skill = ReminderSkill(bus)
    bus.run_forever()