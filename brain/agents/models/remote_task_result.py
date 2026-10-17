
import json
from dataclasses import dataclass

from brain.agents.models.agent_message import (
    AgentMessage,
    AgentMessageType,
)
from brain.agents.models.remote_task_dispatch import RemoteTaskDispatch


@dataclass(frozen=True)
class RemoteTaskResult:
    """A remote outcome correlated with its original dispatch."""

    dispatch_id: str
    task_id: str
    goal_id: str
    workflow_id: str
    workflow_step_id: str
    operation_id: str
    sender_agent_id: str
    recipient_agent_id: str
    status: str
    output: object = None
    error: str | None = None

    def __post_init__(self) -> None:
        for field_name in (
            "dispatch_id",
            "task_id",
            "goal_id",
            "workflow_id",
            "workflow_step_id",
            "operation_id",
            "sender_agent_id",
            "recipient_agent_id",
        ):
            value = getattr(self, field_name)

            if not isinstance(value, str):
                raise TypeError(f"{field_name} must be a string")

            if not value.strip():
                raise ValueError(f"{field_name} must not be empty")

        if self.status not in {"completed", "failed"}:
            raise ValueError(
                "status must be 'completed' or 'failed'"
            )

        if self.status == "completed" and self.error is not None:
            raise ValueError(
                "a completed result cannot contain an error"
            )

        if self.status == "failed":
            if not isinstance(self.error, str) or not self.error.strip():
                raise ValueError(
                    "a failed result must contain a non-empty error"
                )

        try:
            json.dumps(self.output, allow_nan=False)
        except (TypeError, ValueError) as exc:
            raise ValueError(
                "output must contain JSON-compatible values"
            ) from exc

    def to_message(self) -> AgentMessage:
        """Build a response using the existing messaging contract."""

        return AgentMessage(
            id=f"result:{self.dispatch_id}",
            sender_agent_id=self.sender_agent_id,
            recipient_agent_id=self.recipient_agent_id,
            message_type=AgentMessageType.RESPONSE,
            correlation_id=self.dispatch_id,
            payload={
                "kind": "remote_task_result",
                "dispatch_id": self.dispatch_id,
                "task_id": self.task_id,
                "goal_id": self.goal_id,
                "workflow_id": self.workflow_id,
                "workflow_step_id": self.workflow_step_id,
                "operation_id": self.operation_id,
                "status": self.status,
                "output": self.output,
                "error": self.error,
            },
        )

    @classmethod
    def from_message(
        cls,
        message: AgentMessage,
        dispatch: RemoteTaskDispatch,
    ) -> "RemoteTaskResult":
        """Validate a response against the original dispatch."""

        if not isinstance(message, AgentMessage):
            raise TypeError("message must be an AgentMessage")

        if not isinstance(dispatch, RemoteTaskDispatch):
            raise TypeError("dispatch must be a RemoteTaskDispatch")

        if message.message_type is not AgentMessageType.RESPONSE:
            raise ValueError("message must be a RESPONSE")

        if message.correlation_id != dispatch.dispatch_id:
            raise ValueError("response correlation ID does not match dispatch")

        if message.sender_agent_id != dispatch.recipient_agent_id:
            raise ValueError("response sender does not match dispatched agent")

        if message.recipient_agent_id != dispatch.sender_agent_id:
            raise ValueError("response recipient does not match original sender")

        payload = message.payload

        if payload.get("kind") != "remote_task_result":
            raise ValueError("message is not a remote task result")

        expected_references = {
            "dispatch_id": dispatch.dispatch_id,
            "task_id": dispatch.task.id,
            "goal_id": dispatch.goal.id,
            "workflow_id": dispatch.workflow.id,
            "workflow_step_id": dispatch.step.id,
            "operation_id": dispatch.operation.id,
        }

        for field_name, expected_value in expected_references.items():
            if payload.get(field_name) != expected_value:
                raise ValueError(
                    f"response {field_name} does not match dispatch"
                )

        return cls(
            dispatch_id=dispatch.dispatch_id,
            task_id=dispatch.task.id,
            goal_id=dispatch.goal.id,
            workflow_id=dispatch.workflow.id,
            workflow_step_id=dispatch.step.id,
            operation_id=dispatch.operation.id,
            sender_agent_id=message.sender_agent_id,
            recipient_agent_id=message.recipient_agent_id,
            status=payload.get("status"),
            output=payload.get("output"),
            error=payload.get("error"),
        )
