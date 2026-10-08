from abc import ABC, abstractmethod

from brain.agents.models.agent_message import AgentMessage


class AgentCommunicator(ABC):
    """
    Contract for delivering messages between agents.

    This contract does not:
    - execute agents
    - manage agent runtime lifecycle
    - create agents
    - modify agent definitions
    - authorize actions
    - persist messages
    - interpret message payloads
    """

    @abstractmethod
    def send(self, message: AgentMessage) -> None:
        """
        Deliver an agent message.

        Args:
            message: The message to deliver.
        """
        raise NotImplementedError