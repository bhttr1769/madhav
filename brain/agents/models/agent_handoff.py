from dataclasses import dataclass


@dataclass(frozen=True)
class AgentHandoff:
    """
    Represents a handoff of an existing AgentTask from one agent
    to another.

    The handoff is a coordination record. It does not modify the
    AgentTask or AgentAssignment and does not execute the task.
    """

    task_id: str
    from_agent_id: str
    to_agent_id: str
    message_id: str

    def __post_init__(self) -> None:
        if not isinstance(self.task_id, str):
            raise TypeError("task_id must be a string")

        if not self.task_id.strip():
            raise ValueError(
                "task_id must be a non-empty string"
            )

        if not isinstance(self.from_agent_id, str):
            raise TypeError(
                "from_agent_id must be a string"
            )

        if not self.from_agent_id.strip():
            raise ValueError(
                "from_agent_id must be a non-empty string"
            )

        if not isinstance(self.to_agent_id, str):
            raise TypeError(
                "to_agent_id must be a string"
            )

        if not self.to_agent_id.strip():
            raise ValueError(
                "to_agent_id must be a non-empty string"
            )

        if self.from_agent_id == self.to_agent_id:
            raise ValueError(
                "from_agent_id and to_agent_id must be different"
            )

        if not isinstance(self.message_id, str):
            raise TypeError(
                "message_id must be a string"
            )

        if not self.message_id.strip():
            raise ValueError(
                "message_id must be a non-empty string"
            )