from brain.agents.agent_registry import AgentRegistry
from brain.agents.models.agent_message import AgentMessage


class AgentMessageRouter:
    """
    Delivers agent messages to registered agents.

    This component owns message routing and in-memory delivery state.

    It does not:
    - execute agents
    - manage AgentRuntime lifecycle
    - create agents
    - modify AgentDefinitions
    - authorize actions
    - persist messages
    - interpret message payloads
    - manage conversations or threads
    """

    def __init__(self, registry: AgentRegistry) -> None:
        if not isinstance(registry, AgentRegistry):
            raise TypeError("registry must be an AgentRegistry")

        self._registry = registry
        self._messages: dict[str, list[AgentMessage]] = {}

    def send(self, message: AgentMessage) -> None:
        """
        Deliver a message to its registered recipient.

        Raises:
            TypeError: If message is not an AgentMessage.
            ValueError: If the recipient agent is not registered.
        """
        if not isinstance(message, AgentMessage):
            raise TypeError("message must be an AgentMessage")

        if not self._registry.has(message.recipient_agent_id):
            raise ValueError(
                f"Recipient agent is not registered: "
                f"{message.recipient_agent_id}"
            )

        self._messages.setdefault(
            message.recipient_agent_id,
            [],
        ).append(message)

    def messages_for(
        self,
        agent_id: str,
    ) -> tuple[AgentMessage, ...]:
        """
        Return messages delivered to the specified agent.

        The returned collection is immutable from the caller's
        perspective.
        """
        self._validate_agent_id(agent_id)

        return tuple(
            self._messages.get(agent_id, ())
        )

    def messages_for_correlation(
        self,
        agent_id: str,
        correlation_id: str,
    ) -> tuple[AgentMessage, ...]:
        """
        Return messages delivered to an agent that reference
        the supplied correlation ID.

        This method only filters delivered messages. It does not
        interpret message type or enforce request/response semantics.
        """
        self._validate_agent_id(agent_id)

        if not isinstance(correlation_id, str):
            raise TypeError(
                "correlation_id must be a string"
            )

        if not correlation_id.strip():
            raise ValueError(
                "correlation_id must be a non-empty string"
            )

        return tuple(
            message
            for message in self._messages.get(agent_id, ())
            if message.correlation_id == correlation_id
        )

    @staticmethod
    def _validate_agent_id(agent_id: str) -> None:
        if not isinstance(agent_id, str):
            raise TypeError("agent_id must be a string")

        if not agent_id.strip():
            raise ValueError(
                "agent_id must be a non-empty string"
            )