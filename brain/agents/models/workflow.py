from dataclasses import dataclass
from enum import Enum


class WorkflowStatus(Enum):
    """
    Defines the lifecycle state of a workflow.
    """

    CREATED = "created"
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(frozen=True)
class Workflow:
    """
    Represents the definition and lifecycle state of a workflow.

    A workflow references existing workflow step IDs rather than
    storing or duplicating WorkflowStep objects.

    The workflow does not execute tasks, select agents, manage
    runtimes, or perform persistence.
    """

    id: str
    goal_id: str
    step_ids: tuple[str, ...]
    status: WorkflowStatus = WorkflowStatus.CREATED

    def __post_init__(self) -> None:
        if not isinstance(self.id, str):
            raise TypeError("id must be a string")

        if not self.id.strip():
            raise ValueError("id must be a non-empty string")

        if not isinstance(self.goal_id, str):
            raise TypeError("goal_id must be a string")

        if not self.goal_id.strip():
            raise ValueError(
                "goal_id must be a non-empty string"
            )

        if not isinstance(self.step_ids, tuple):
            raise TypeError("step_ids must be a tuple")

        for step_id in self.step_ids:
            if not isinstance(step_id, str):
                raise TypeError(
                    "step_ids must contain only strings"
                )

            if not step_id.strip():
                raise ValueError(
                    "step_ids must contain only non-empty strings"
                )

        if len(self.step_ids) != len(set(self.step_ids)):
            raise ValueError(
                "step_ids must not contain duplicate step IDs"
            )

        if not isinstance(self.status, WorkflowStatus):
            raise TypeError(
                "status must be a WorkflowStatus"
            )