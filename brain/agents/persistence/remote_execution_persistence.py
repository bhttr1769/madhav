
from abc import ABC, abstractmethod

from brain.agents.models.remote_execution_record import (
    RemoteExecutionRecord,
)


class RemoteExecutionPersistence(ABC):
    """Persistence contract for remote dispatch ownership and outcomes."""

    @abstractmethod
    def claim(self, record: RemoteExecutionRecord) -> bool:
        """Atomically create the initial record if the dispatch is new."""
        raise NotImplementedError

    @abstractmethod
    def load(self, dispatch_id: str) -> RemoteExecutionRecord:
        """Load a dispatch record by ID."""
        raise NotImplementedError

    @abstractmethod
    def save(self, record: RemoteExecutionRecord) -> None:
        """Persist an allowed state transition."""
        raise NotImplementedError

    @abstractmethod
    def all(self) -> tuple[RemoteExecutionRecord, ...]:
        """Return all persisted dispatch records."""
        raise NotImplementedError
