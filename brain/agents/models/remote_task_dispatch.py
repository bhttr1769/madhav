
import json
from dataclasses import dataclass, field

from brain.agents.models.agent_message import (
    AgentMessage,
    AgentMessageType,
)
from brain.agents.models.agent_operation import (
    AgentOperation,
    AgentOperationStatus,
)
from brain.agents.models.agent_task import AgentTask
from brain.agents.models.agent_task_status import AgentTaskStatus
from brain.agents.models.goal import Goal
from brain.agents.models.goal_status import GoalStatus
from brain.agents.models.workflow import Workflow, WorkflowStatus
from brain.agents.models.workflow_step import (
    WorkflowStep,
    WorkflowStepStatus,
)


@dataclass(frozen=True)
class RemoteTaskDispatch:
    """A validated request to dispatch an existing task remotely."""

    dispatch_id: str
    sender_agent_id: str
    recipient_agent_id: str
    recipient_node_id: str
    operation: AgentOperation
    goal: Goal
    workflow: Workflow
    step: WorkflowStep
    task: AgentTask
    capability_id: str
    input_payload: dict[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for field_name in (
            "dispatch_id",
            "sender_agent_id",
            "recipient_agent_id",
            "recipient_node_id",
        ):
            value = getattr(self, field_name)

            if not isinstance(value, str):
                raise TypeError(f"{field_name} must be a string")

            if not value.strip():
                raise ValueError(f"{field_name} must not be empty")

        if self.sender_agent_id == self.recipient_agent_id:
            raise ValueError(
                "sender and recipient agents must be different"
            )

        expected_types = (
            ("operation", self.operation, AgentOperation),
            ("goal", self.goal, Goal),
            ("workflow", self.workflow, Workflow),
            ("step", self.step, WorkflowStep),
            ("task", self.task, AgentTask),
        )

        for field_name, value, expected_type in expected_types:
            if not isinstance(value, expected_type):
                raise TypeError(
                    f"{field_name} must be a {expected_type.__name__}"
                )

        if not isinstance(self.input_payload, dict):
            raise TypeError("input_payload must be a dictionary")

        if any(
            not isinstance(key, str)
            for key in self.input_payload
        ):
            raise TypeError("input_payload keys must be strings")

        # Reuse the existing domain models and verify their references.
        if self.operation.goal_id != self.goal.id:
            raise ValueError("operation does not reference the supplied goal")

        if self.operation.workflow_id != self.workflow.id:
            raise ValueError(
                "operation does not reference the supplied workflow"
            )

        if self.workflow.goal_id != self.goal.id:
            raise ValueError("workflow does not reference the supplied goal")

        if self.task.goal_id != self.goal.id:
            raise ValueError("task does not belong to the supplied goal")

        if self.step.task_id != self.task.id:
            raise ValueError("workflow step does not reference the supplied task")

        if self.step.id not in self.workflow.step_ids:
            raise ValueError("workflow does not contain the supplied step")

        # Dispatch only work that the existing lifecycle has started.
        if self.operation.status is not AgentOperationStatus.RUNNING:
            raise ValueError("operation must be RUNNING")

        if self.goal.status is not GoalStatus.ACTIVE:
            raise ValueError("goal must be ACTIVE")

        if self.workflow.status is not WorkflowStatus.RUNNING:
            raise ValueError("workflow must be RUNNING")

        if self.step.status is not WorkflowStepStatus.RUNNING:
            raise ValueError("workflow step must be RUNNING")

        if self.task.status is not AgentTaskStatus.ACTIVE:
            raise ValueError("task must be ACTIVE")

        if not isinstance(self.capability_id, str):
            raise TypeError("capability_id must be a string")
        if not self.capability_id.strip():
            raise ValueError("capability_id must not be empty")  

        # Fail before transport if the input cannot be represented as JSON.
        try:
            json.dumps(
                self.input_payload,
                allow_nan=False,
            )
        except (TypeError, ValueError) as exc:
            raise ValueError(
                "input_payload must contain JSON-compatible values"
            ) from exc

    def to_message(self) -> AgentMessage:
        """Build the existing AgentMessage request envelope."""

        payload: dict[str, object] = {
            "kind": "remote_task_dispatch",
            "dispatch_id": self.dispatch_id,
            "operation_id": self.operation.id,
            "goal_id": self.goal.id,
            "workflow_id": self.workflow.id,
            "workflow_step_id": self.step.id,
            "task_id": self.task.id,
            "task_description": self.task.description,
            "goal_description": self.goal.description,
            "dependencies": sorted(self.task.dependencies),
            "input": self.input_payload,
            "capability_id": self.capability_id,
        }

        return AgentMessage(
            id=f"dispatch:{self.dispatch_id}",
            sender_agent_id=self.sender_agent_id,
            recipient_agent_id=self.recipient_agent_id,
            message_type=AgentMessageType.REQUEST,
            payload=payload,
            correlation_id=self.dispatch_id,
        )
