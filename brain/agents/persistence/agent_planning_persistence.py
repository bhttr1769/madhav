from abc import ABC, abstractmethod

from brain.agents.models.agent_planning_persistence_state import (
    AgentPlanningPersistenceState,
)


class AgentPlanningPersistence(ABC):
    """
    Persistence contract for agent planning and delegation state.

    This contract defines persistence only. It does not provide
    a storage backend or perform planning, delegation, or execution.
    """

    @abstractmethod
    def save(
        self,
        state: AgentPlanningPersistenceState,
    ) -> None:
        """
        Persist planning state.
        """
        raise NotImplementedError

    @abstractmethod
    def load(
        self,
        goal_id: str,
    ) -> AgentPlanningPersistenceState:
        """
        Restore planning state for a goal.
        """
        raise NotImplementedError