from dataclasses import replace

from brain.agents.models.agent_operation import (
    AgentOperation,
    AgentOperationStatus,
)


class AgentOperationLifecycle:
    """Manages valid lifecycle transitions for an agent operation."""

    _ALLOWED_TRANSITIONS = {
        AgentOperationStatus.CREATED: frozenset({
            AgentOperationStatus.RUNNING,
            AgentOperationStatus.CANCELLED,
        }),
        AgentOperationStatus.RUNNING: frozenset({
            AgentOperationStatus.PAUSED,
            AgentOperationStatus.COMPLETED,
            AgentOperationStatus.FAILED,
            AgentOperationStatus.CANCELLED,
        }),
        AgentOperationStatus.PAUSED: frozenset({
            AgentOperationStatus.RUNNING,
            AgentOperationStatus.FAILED,
            AgentOperationStatus.CANCELLED,
        }),
        AgentOperationStatus.COMPLETED: frozenset(),
        AgentOperationStatus.FAILED: frozenset(),
        AgentOperationStatus.CANCELLED: frozenset(),
    }

    def can_transition(
        self,
        current_status: AgentOperationStatus,
        target_status: AgentOperationStatus,
    ) -> bool:
        """Return whether a status transition is permitted."""
        self._validate_status(current_status, "current_status")
        self._validate_status(target_status, "target_status")

        return target_status in self._ALLOWED_TRANSITIONS[current_status]

    def transition(
        self,
        operation: AgentOperation,
        target_status: AgentOperationStatus,
    ) -> AgentOperation:
        """Return a new operation with the requested valid status."""
        if not isinstance(operation, AgentOperation):
            raise TypeError("operation must be an AgentOperation")

        self._validate_status(target_status, "target_status")

        if not self.can_transition(operation.status, target_status):
            raise ValueError(
                f"Invalid operation status transition: "
                f"{operation.status.value} -> {target_status.value}"
            )

        return replace(operation, status=target_status)

    @staticmethod
    def _validate_status(
        status: AgentOperationStatus,
        field_name: str,
    ) -> None:
        if not isinstance(status, AgentOperationStatus):
            raise TypeError(
                f"{field_name} must be an AgentOperationStatus"
            )