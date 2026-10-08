from typing import Protocol, runtime_checkable

from brain.agents.models.workflow_persistence_state import (
    WorkflowPersistenceState,
)


@runtime_checkable
class WorkflowPersistence(Protocol):
    def save(
        self,
        state: WorkflowPersistenceState,
    ) -> None:
        ...

    def load(
        self,
        workflow_id: str,
    ) -> WorkflowPersistenceState:
        ...