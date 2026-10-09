from brain.agents.agent_operation_lifecycle import AgentOperationLifecycle
from brain.agents.models.agent_operation import (
    AgentOperation,
    AgentOperationStatus,
)
from brain.agents.models.goal import Goal
from brain.agents.models.workflow import Workflow


class AgentOperationCoordinator:
    """Coordinates operation lifecycle against existing goal and workflow state."""

    def __init__(
        self,
        lifecycle: AgentOperationLifecycle | None = None,
    ) -> None:
        if lifecycle is None:
            lifecycle = AgentOperationLifecycle()

        if not isinstance(lifecycle, AgentOperationLifecycle):
            raise TypeError(
                "lifecycle must be an AgentOperationLifecycle"
            )

        self._lifecycle = lifecycle

    def validate(
        self,
        operation: AgentOperation,
        goal: Goal,
        workflow: Workflow,
    ) -> None:
        """Validate that an operation references its matching goal and workflow."""
        if not isinstance(operation, AgentOperation):
            raise TypeError("operation must be an AgentOperation")

        if not isinstance(goal, Goal):
            raise TypeError("goal must be a Goal")

        if not isinstance(workflow, Workflow):
            raise TypeError("workflow must be a Workflow")

        if operation.goal_id != goal.id:
            raise ValueError(
                "operation goal_id must match the provided goal"
            )

        if operation.workflow_id != workflow.id:
            raise ValueError(
                "operation workflow_id must match the provided workflow"
            )

        if workflow.goal_id != goal.id:
            raise ValueError(
                "workflow goal_id must match the provided goal"
            )

    def start(
        self,
        operation: AgentOperation,
        goal: Goal,
        workflow: Workflow,
    ) -> AgentOperation:
        """Start an operation after validating its references."""
        self.validate(operation, goal, workflow)

        if workflow.status.value not in {"ready", "running"}:
            raise ValueError(
                "workflow must be READY or RUNNING to start an operation"
            )

        return self._lifecycle.transition(
            operation,
            AgentOperationStatus.RUNNING,
        )

    def pause(
        self,
        operation: AgentOperation,
        goal: Goal,
        workflow: Workflow,
    ) -> AgentOperation:
        """Pause a running operation."""
        self.validate(operation, goal, workflow)

        return self._lifecycle.transition(
            operation,
            AgentOperationStatus.PAUSED,
        )

    def resume(
        self,
        operation: AgentOperation,
        goal: Goal,
        workflow: Workflow,
    ) -> AgentOperation:
        """Resume a paused operation."""
        self.validate(operation, goal, workflow)

        if workflow.status.value != "running":
            raise ValueError(
                "workflow must be RUNNING to resume an operation"
            )

        return self._lifecycle.transition(
            operation,
            AgentOperationStatus.RUNNING,
        )

    def complete(
        self,
        operation: AgentOperation,
        goal: Goal,
        workflow: Workflow,
    ) -> AgentOperation:
        """Complete an operation only after its workflow completes."""
        self.validate(operation, goal, workflow)

        if workflow.status.value != "completed":
            raise ValueError(
                "workflow must be COMPLETED to complete an operation"
            )

        return self._lifecycle.transition(
            operation,
            AgentOperationStatus.COMPLETED,
        )

    def fail(
        self,
        operation: AgentOperation,
        goal: Goal,
        workflow: Workflow,
    ) -> AgentOperation:
        """Mark an operation failed when its workflow has failed."""
        self.validate(operation, goal, workflow)

        if workflow.status.value != "failed":
            raise ValueError(
                "workflow must be FAILED to fail an operation"
            )

        return self._lifecycle.transition(
            operation,
            AgentOperationStatus.FAILED,
        )

    def cancel(
        self,
        operation: AgentOperation,
        goal: Goal,
        workflow: Workflow,
    ) -> AgentOperation:
        """Cancel an operation without modifying its workflow or goal."""
        self.validate(operation, goal, workflow)

        return self._lifecycle.transition(
            operation,
            AgentOperationStatus.CANCELLED,
        )