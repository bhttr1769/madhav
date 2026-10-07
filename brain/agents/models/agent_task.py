from dataclasses import dataclass

from brain.agents.models.agent_task_status import AgentTaskStatus


@dataclass(frozen=True)
class AgentTask:
    id: str
    goal_id: str
    description: str
    parent_task_id: str | None = None
    dependencies: frozenset[str] = frozenset()
    status: AgentTaskStatus = AgentTaskStatus.CREATED
    progress: int = 0

    def __post_init__(self) -> None:
        if not isinstance(self.id, str):
            raise TypeError("id must be a string")
        if not self.id.strip():
            raise ValueError("id must not be empty")

        if not isinstance(self.goal_id, str):
            raise TypeError("goal_id must be a string")
        if not self.goal_id.strip():
            raise ValueError("goal_id must not be empty")

        if not isinstance(self.description, str):
            raise TypeError("description must be a string")
        if not self.description.strip():
            raise ValueError("description must not be empty")

        if self.parent_task_id is not None:
            if not isinstance(self.parent_task_id, str):
                raise TypeError(
                    "parent_task_id must be a string or None"
                )
            if not self.parent_task_id.strip():
                raise ValueError(
                    "parent_task_id must not be empty"
                )

            if self.parent_task_id == self.id:
                raise ValueError(
                    "parent_task_id must not reference the task itself"
                )

        if not isinstance(self.dependencies, frozenset):
            raise TypeError(
                "dependencies must be a frozenset"
            )

        for dependency_id in self.dependencies:
            if not isinstance(dependency_id, str):
                raise TypeError(
                    "dependency IDs must be strings"
                )
            if not dependency_id.strip():
                raise ValueError(
                    "dependency IDs must not be empty"
                )
            if dependency_id == self.id:
                raise ValueError(
                    "task must not depend on itself"
                )

        if not isinstance(self.status, AgentTaskStatus):
            raise TypeError(
                "status must be an AgentTaskStatus"
            )

        if isinstance(self.progress, bool) or not isinstance(self.progress, int):
            raise TypeError(
                "progress must be an integer"
            )

        if not 0 <= self.progress <= 100:
            raise ValueError(
                "progress must be between 0 and 100"
            )

        if self.status is AgentTaskStatus.COMPLETED:
            if self.progress != 100:
                raise ValueError(
                    "completed task must have progress of 100"
                )
        elif self.status in {
            AgentTaskStatus.CREATED,
            AgentTaskStatus.ACTIVE,
            AgentTaskStatus.FAILED,
            AgentTaskStatus.CANCELLED,
        } and self.progress == 100:
            raise ValueError(
                "only a completed task can have progress of 100"
            )

        if (
            self.status is AgentTaskStatus.CREATED
            and self.progress != 0
        ):
            raise ValueError(
                "created task must have progress of 0"
            )