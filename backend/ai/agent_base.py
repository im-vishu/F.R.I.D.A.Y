class AgentBase:
    """
    Base class for all agents; provides publish/subscribe interface to the event bus.
    """
    def __init__(self, agent_name, event_bus):
        self.agent_name = agent_name
        self.bus = event_bus

    def publish(self, type_, payload, target="broadcast"):
        """
        Publish an event to the event bus.
        """
        event = {
            "origin": self.agent_name,
            "type": type_,
            "payload": payload,
            "target": target
        }
        self.bus.publish_event(type_, event)

    def on_event(self, type_, handler):
        self.bus.subscribe_event(type_, handler)