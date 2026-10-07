from typing import Protocol

from brain.agents.models.context_restoration_state import (
    ContextRestorationState,
)


class ContextPersistence(Protocol):
    def save(
        self,
        state: ContextRestorationState,
    ) -> None:
        ...

    def load(
        self,
        runtime_id: str,
    ) -> ContextRestorationState:
        ...