from dataclasses import dataclass

from brain.agents.models.agent_handoff import AgentHandoff
from brain.agents.models.agent_message import AgentMessage


@dataclass(frozen=True)
class AgentCommunicationPersistenceState:
    """
    Persistable communication state.

    Contains delivered agent messages and handoff records.
    The state represents data only; it does not perform routing,
    communication, execution, or persistence.
    """

    messages: tuple[AgentMessage, ...]
    handoffs: tuple[AgentHandoff, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.messages, tuple):
            raise TypeError("messages must be a tuple")

        for message in self.messages:
            if not isinstance(message, AgentMessage):
                raise TypeError(
                    "messages must contain only AgentMessage instances"
                )

        if not isinstance(self.handoffs, tuple):
            raise TypeError("handoffs must be a tuple")

        for handoff in self.handoffs:
            if not isinstance(handoff, AgentHandoff):
                raise TypeError(
                    "handoffs must contain only AgentHandoff instances"
                )