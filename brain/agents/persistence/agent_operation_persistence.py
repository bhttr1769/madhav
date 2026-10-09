from abc import ABC, abstractmethod

from brain.agents.models.agent_operation_checkpoint_state import (
    AgentOperationCheckpointState,
)


class AgentOperationPersistence(ABC):
    """Persistence contract for long-running agent operations."""

    @abstractmethod
    def save(
        self,
        state: AgentOperationCheckpointState,
    ) -> None:
        """Persist an operation checkpoint."""
        raise NotImplementedError

    @abstractmethod
    def load(
        self,
        operation_id: str,
    ) -> AgentOperationCheckpointState:
        """Load a checkpoint by operation ID."""
        raise NotImplementedError