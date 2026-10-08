from typing import Protocol, runtime_checkable

from brain.agents.models.agent_performance_persistence_state import (
    AgentPerformancePersistenceState,
)


@runtime_checkable
class AgentPerformancePersistence(Protocol):
    def save(
        self,
        state: AgentPerformancePersistenceState,
    ) -> None:
        ...

    def load(
        self,
        agent_id: str,
    ) -> AgentPerformancePersistenceState:
        ...