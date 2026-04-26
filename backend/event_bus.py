import threading
import queue
import time
import sys

class LogColors:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    END = "\033[0m"
    BOLD = "\033[1m"

def log(message, level="info"):
    color = {
        "info": LogColors.GREEN,
        "debug": LogColors.BLUE,
        "warning": LogColors.YELLOW,
        "error": LogColors.RED,
        "event": LogColors.CYAN
    }.get(level, LogColors.END)
    print(f"{color}[{level.upper()}]{LogColors.END} {message}")

class EventBus:
    def __init__(self):
        self._handlers = {}
        self._event_queue = queue.Queue()
        self._running = False

    def subscribe(self, event_name, handler):
        if event_name not in self._handlers:
            self._handlers[event_name] = []
        self._handlers[event_name].append(handler)
        log(f"Subscribed handler {handler.__qualname__} to '{event_name}'", "debug")

    def publish(self, event_name, payload):
        self._event_queue.put({
            "event_name": event_name,
            "payload": payload
        })
        log(f"Event published: {event_name}", "event")

    def publish_event(self, event_name, event):
        self.publish(event_name, event["payload"])

    def _handle_event(self, event_name, payload):
        handlers = self._handlers.get(event_name, [])
        for handler in handlers:
            threading.Thread(target=handler, args=({"payload": payload},), daemon=True).start()
            log(f"Dispatched event '{event_name}' to {handler.__qualname__}", "debug")

    def run_forever(self):
        self._running = True
        log("EventBus running (threaded)...", "info")
        try:
            while self._running:
                try:
                    event = self._event_queue.get(timeout=0.2)
                    self._handle_event(event["event_name"], event["payload"])
                except queue.Empty:
                    continue
        except KeyboardInterrupt:
            log("KeyboardInterrupt: shutting down EventBus.", "warning")
            self._running = False
        except Exception as exc:
            log(f"Exception in EventBus main loop: {exc}", "error")
            self._running = False

    def stop(self):
        self._running = False