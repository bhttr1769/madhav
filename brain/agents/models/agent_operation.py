from dataclasses import dataclass
from enum import Enum


class AgentOperationStatus(Enum):
    CREATED = "created"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class AgentOperation:
    id: str
    goal_id: str
    workflow_id: str
    status: AgentOperationStatus = AgentOperationStatus.CREATED

    def __post_init__(self) -> None:
        for field_name, value in (
            ("id", self.id),
            ("goal_id", self.goal_id),
            ("workflow_id", self.workflow_id),
        ):
            if not isinstance(value, str):
                raise TypeError(f"{field_name} must be a string")

            if not value.strip():
                raise ValueError(f"{field_name} must not be empty")

        if not isinstance(self.status, AgentOperationStatus):
            raise TypeError(
                "status must be an AgentOperationStatus"
            )