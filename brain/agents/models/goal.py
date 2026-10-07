from dataclasses import dataclass

from brain.agents.models.goal_status import GoalStatus


@dataclass(frozen=True)
class Goal:
    id: str
    agent_id: str
    description: str
    status: GoalStatus = GoalStatus.CREATED
    progress: int = 0

    def __post_init__(self) -> None:
        if not isinstance(self.id, str):
            raise TypeError("id must be a string")
        if not self.id.strip():
            raise ValueError("id must not be empty")

        if not isinstance(self.agent_id, str):
            raise TypeError("agent_id must be a string")
        if not self.agent_id.strip():
            raise ValueError("agent_id must not be empty")

        if not isinstance(self.description, str):
            raise TypeError("description must be a string")
        if not self.description.strip():
            raise ValueError("description must not be empty")

        if not isinstance(self.status, GoalStatus):
            raise TypeError("status must be a GoalStatus")

        if isinstance(self.progress, bool) or not isinstance(self.progress, int):
            raise TypeError("progress must be an integer")

        if not 0 <= self.progress <= 100:
            raise ValueError("progress must be between 0 and 100")

        if self.status is GoalStatus.COMPLETED:
            if self.progress != 100:
                raise ValueError(
                    "completed goal must have progress of 100"
                )
        elif self.status in {
            GoalStatus.CREATED,
            GoalStatus.ACTIVE,
            GoalStatus.FAILED,
            GoalStatus.CANCELLED,
        } and self.progress == 100:
            raise ValueError(
                "only a completed goal can have progress of 100"
            )

        if self.status is GoalStatus.CREATED and self.progress != 0:
            raise ValueError(
                "created goal must have progress of 0"
            )