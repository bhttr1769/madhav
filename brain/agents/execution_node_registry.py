
from brain.agents.models.execution_node_registration import (
    ExecutionNodeRegistration,
)


class ExecutionNodeRegistry:
    """In-memory registry of execution-node registrations."""

    def __init__(
        self,
        registrations: tuple[ExecutionNodeRegistration, ...] = (),
    ) -> None:
        self._registrations: dict[str, ExecutionNodeRegistration] = {}

        for registration in registrations:
            self.register(registration)

    def register(self, registration: ExecutionNodeRegistration) -> None:
        if not isinstance(registration, ExecutionNodeRegistration):
            raise TypeError(
                "registration must be an ExecutionNodeRegistration"
            )

        node_id = registration.node_id

        if node_id in self._registrations:
            raise ValueError(
                f"execution node already registered: {node_id}"
            )

        self._registrations[node_id] = registration

    def get(self, node_id: str) -> ExecutionNodeRegistration:
        self._validate_node_id(node_id)

        try:
            return self._registrations[node_id]
        except KeyError as exc:
            raise KeyError(
                f"execution node not found: {node_id}"
            ) from exc

    def has(self, node_id: str) -> bool:
        self._validate_node_id(node_id)
        return node_id in self._registrations

    def all(self) -> tuple[ExecutionNodeRegistration, ...]:
        return tuple(self._registrations.values())

    def unregister(self, node_id: str) -> None:
        self._validate_node_id(node_id)

        if node_id not in self._registrations:
            raise KeyError(
                f"execution node not found: {node_id}"
            )

        del self._registrations[node_id]

    @staticmethod
    def _validate_node_id(node_id: str) -> None:
        if not isinstance(node_id, str):
            raise TypeError("node_id must be a string")

        if not node_id.strip():
            raise ValueError("node_id must not be empty")
