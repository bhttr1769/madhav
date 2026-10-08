from dataclasses import dataclass
from enum import Enum


class WorkflowStepStatus(Enum):
    """
    Defines the lifecycle state of a workflow step.
    """

    PENDING = "pending"
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(frozen=True)
class WorkflowStep:
    """
    Represents one step within a Workflow.

    The step references an existing AgentTask rather than
    duplicating task information.

    It does not execute the task, modify the task lifecycle,
    select an agent, or manage an AgentRuntime.
    """

    id: str
    task_id: str
    status: WorkflowStepStatus = WorkflowStepStatus.PENDING

    def __post_init__(self) -> None:
        if not isinstance(self.id, str):
            raise TypeError("id must be a string")

        if not self.id.strip():
            raise ValueError("id must be a non-empty string")

        if not isinstance(self.task_id, str):
            raise TypeError("task_id must be a string")

        if not self.task_id.strip():
            raise ValueError(
                "task_id must be a non-empty string"
            )

        if not isinstance(self.status, WorkflowStepStatus):
            raise TypeError(
                "status must be a WorkflowStepStatus"
            )