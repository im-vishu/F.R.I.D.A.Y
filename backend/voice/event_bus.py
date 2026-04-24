def publish_event(event_type, data):
    print(f"[EVENT BUS] {event_type}: {data}")

def subscribe_event(event_type):
    def decorator(func):
        # Placeholder for later real event hooks
        return func
    return decorator