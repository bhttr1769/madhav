from typing import Protocol

from brain.agents.models.goal_task_persistence_state import (
    GoalTaskPersistenceState,
)


class GoalTaskPersistence(Protocol):
    def save(
        self,
        state: GoalTaskPersistenceState,
    ) -> None:
        ...

    def load(
        self,
        agent_id: str,
    ) -> GoalTaskPersistenceState:
        ...