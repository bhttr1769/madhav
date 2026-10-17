
from dataclasses import dataclass


@dataclass(frozen=True)
class ExecutionNodeIdentity:
    """Stable identity for an execution node."""

    node_id: str

    def __post_init__(self) -> None:
        if not isinstance(self.node_id, str):
            raise TypeError("node_id must be a string")

        if not self.node_id.strip():
            raise ValueError("node_id must not be empty")
