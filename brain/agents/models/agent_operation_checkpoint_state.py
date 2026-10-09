from dataclasses import dataclass

from brain.agents.models.agent_operation import AgentOperation


@dataclass(frozen=True)
class AgentOperationCheckpointState:
    """
    Continuation state for a long-running agent operation.

    Stores operation identity and references to the existing goal
    and workflow. It does not duplicate their state or implement
    checkpointing, persistence, or recovery.
    """

    operation: AgentOperation

    def __post_init__(self) -> None:
        if not isinstance(self.operation, AgentOperation):
            raise TypeError(
                "operation must be an AgentOperation"
            )