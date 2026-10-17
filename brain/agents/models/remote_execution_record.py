
from dataclasses import dataclass
from enum import Enum

from brain.agents.models.agent_message import AgentMessage


class RemoteExecutionStatus(str, Enum):
    CLAIMED = "claimed"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    UNCERTAIN = "uncertain"


@dataclass(frozen=True)
class RemoteExecutionRecord:
    dispatch_id: str
    request_fingerprint: str
    owner_node_id: str
    status: RemoteExecutionStatus
    response: AgentMessage | None = None

    def __post_init__(self) -> None:
        for name in (
            "dispatch_id",
            "request_fingerprint",
            "owner_node_id",
        ):
            value = getattr(self, name)
            if not isinstance(value, str):
                raise TypeError(f"{name} must be a string")
            if not value.strip():
                raise ValueError(f"{name} must not be empty")

        if not isinstance(self.status, RemoteExecutionStatus):
            raise TypeError(
                "status must be a RemoteExecutionStatus"
            )

        if self.response is not None and not isinstance(
            self.response,
            AgentMessage,
        ):
            raise TypeError("response must be an AgentMessage or None")

        terminal = {
            RemoteExecutionStatus.COMPLETED,
            RemoteExecutionStatus.FAILED,
        }
        if self.status in terminal and self.response is None:
            raise ValueError(
                "completed and failed records require a response"
            )

        if self.status in {
            RemoteExecutionStatus.CLAIMED,
            RemoteExecutionStatus.RUNNING,
            RemoteExecutionStatus.UNCERTAIN,
        } and self.response is not None:
            raise ValueError(
                "non-terminal records must not contain a response"
            )
