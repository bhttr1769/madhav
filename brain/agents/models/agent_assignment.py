from dataclasses import dataclass


@dataclass(frozen=True)
class AgentAssignment:
    """
    Represents the assignment of an existing AgentTask
    to an existing AgentDefinition.

    This model stores references only. It does not perform
    agent selection, capability validation, task execution,
    or runtime management.
    """

    task_id: str
    agent_id: str

    def __post_init__(self) -> None:
        if not isinstance(self.task_id, str):
            raise TypeError("task_id must be a string")

        if not self.task_id.strip():
            raise ValueError("task_id must be a non-empty string")

        if not isinstance(self.agent_id, str):
            raise TypeError("agent_id must be a string")

        if not self.agent_id.strip():
            raise ValueError("agent_id must be a non-empty string")