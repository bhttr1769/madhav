
from dataclasses import dataclass

from brain.agents.models.execution_node_identity import ExecutionNodeIdentity


@dataclass(frozen=True)
class ExecutionNodeRegistration:
    """Registration details for a node that may host agent execution."""

    identity: ExecutionNodeIdentity
    endpoint: str

    def __post_init__(self) -> None:
        if not isinstance(self.identity, ExecutionNodeIdentity):
            raise TypeError("identity must be an ExecutionNodeIdentity")

        if not isinstance(self.endpoint, str):
            raise TypeError("endpoint must be a string")

        if not self.endpoint.strip():
            raise ValueError("endpoint must not be empty")

    @property
    def node_id(self) -> str:
        return self.identity.node_id
