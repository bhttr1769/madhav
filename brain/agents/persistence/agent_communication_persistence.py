from abc import ABC, abstractmethod

from brain.agents.models.agent_communication_persistence_state import (
    AgentCommunicationPersistenceState,
)


class AgentCommunicationPersistence(ABC):
    """
    Persistence contract for agent communication state.

    This contract defines persistence only. It does not provide
    a storage backend or perform routing, communication,
    execution, or handoff processing.
    """

    @abstractmethod
    def save(
        self,
        state: AgentCommunicationPersistenceState,
    ) -> None:
        """
        Persist communication state.
        """
        raise NotImplementedError

    @abstractmethod
    def load(
        self,
    ) -> AgentCommunicationPersistenceState:
        """
        Restore communication state.
        """
        raise NotImplementedError