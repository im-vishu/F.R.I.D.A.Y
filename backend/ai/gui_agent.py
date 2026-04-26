import tkinter as tk
import threading
from backend.ai.agent_base import AgentBase

class GUIAgent(AgentBase):
    def __init__(self, event_bus):
        super().__init__("gui", event_bus)
        self.root = tk.Tk()
        self.root.title("F.R.I.D.A.Y Chat")

        # GUI layout
        self.out_text = tk.Text(self.root, wrap=tk.WORD, height=24, width=72, state=tk.DISABLED)
        self.out_text.pack(padx=6, pady=6)
        self.entry = tk.Entry(self.root, width=72)
        self.entry.pack(padx=6, pady=(0,6))
        self.entry.bind("<Return>", self.send_user_input)

        # Subscribe to all skill results for display
        skills = [
            "skills.weather.result", "skills.wikipedia.result", "skills.joke.result", "skills.reminder.result",
            "skills.calculator.result", "skills.quote.result", "skills.news.result", "skills.code.result"
        ]
        for event in skills:
            self.on_event(event, self.display_result)
        self.insert("F.R.I.D.A.Y online. Type a request and press ENTER.")

    def insert(self, msg):
        self.out_text.config(state=tk.NORMAL)
        self.out_text.insert(tk.END, msg + "\n")
        self.out_text.see(tk.END)
        self.out_text.config(state=tk.DISABLED)

    def send_user_input(self, event=None):
        text = self.entry.get().strip()
        self.entry.delete(0, tk.END)
        if text:
            self.insert(f"You: {text}")
            self.publish("stt.result", {"text": text})

    def display_result(self, event):
        answer = event["payload"].get("result") or event["payload"].get("text")
        if answer:
            self.insert(f"F.R.I.D.A.Y: {answer}")

    def start_mainloop(self):
        threading.Thread(target=self.root.mainloop, daemon=True).start()

if __name__ == "__main__":
    from backend.event_bus import EventBus
    bus = EventBus()
    gui = GUIAgent(bus)
    gui.start_mainloop()
    bus.run_forever()