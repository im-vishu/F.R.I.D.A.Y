import queue

class EventBus:
    def __init__(self):
        self.listeners = {}
        self.q = queue.Queue()

    def publish_event(self, type_, event):
        print(f"[EVENT BUS] {type_} -> {event.get('target', 'broadcast')}: {event['payload']}")
        self.q.put((type_, event))

    def subscribe_event(self, type_, handler):
        self.listeners.setdefault(type_, []).append(handler)

    def run_forever(self):
        while True:
            type_, event = self.q.get()
            for handler in self.listeners.get(type_, []):
                handler(event)