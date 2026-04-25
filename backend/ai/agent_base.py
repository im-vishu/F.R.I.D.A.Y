class AgentBase:
    """
    Base class for all F.R.I.D.A.Y agents.
    Provides publish/subscribe interface to the centralized event bus.
    """

    def __init__(self, agent_name, event_bus):
        """
        Initialize an agent.
        :param agent_name: Unique string name/ID for this agent.
        :param event_bus: Shared EventBus instance for publish/subscribe.
        """
        self.agent_name = agent_name
        self.bus = event_bus

    def publish(self, type_, payload, target="broadcast"):
        """
        Publish an event to the event bus.
        :param type_: Event type (string).
        :param payload: Arbitrary Python object as event content.
        :param target: (Optional) target recipient (agent name) or 'broadcast'.
        """
        event = {
            "origin": self.agent_name,
            "type": type_,
            "payload": payload,
            "target": target
        }
        self.bus.publish_event(type_, event)

    def on_event(self, type_, handler):
        """
        Subscribe to a specific event type, using a handler callback.
        :param type_: Event type (string) to subscribe to.
        :param handler: Function to handle the event (called with event dict).
        """
        self.bus.subscribe_event(type_, handler)