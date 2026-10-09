
from brain.agents.agent_operation_coordinator import AgentOperationCoordinator
from brain.agents.models.agent_operation import (
    AgentOperation,
    AgentOperationStatus,
)
from brain.agents.models.agent_task import AgentTask
from brain.agents.models.goal import Goal
from brain.agents.models.goal_task_persistence_state import (
    GoalTaskPersistenceState,
)
from brain.agents.models.workflow import Workflow, WorkflowStatus
from brain.agents.models.workflow_persistence_state import (
    WorkflowPersistenceState,
)
from brain.agents.models.workflow_step import (
    WorkflowStep,
    WorkflowStepStatus,
)
from brain.agents.persistence.agent_operation_persistence import (
    AgentOperationPersistence,
)
from brain.agents.goal_task_persistence import GoalTaskPersistence
from brain.agents.workflow_persistence import WorkflowPersistence


class AgentOperationRestorationCoordinator:
    """Load and validate persisted operation state without resuming it."""

    def __init__(
        self,
        operation_persistence: AgentOperationPersistence,
        goal_task_persistence: GoalTaskPersistence,
        workflow_persistence: WorkflowPersistence,
        operation_coordinator: AgentOperationCoordinator | None = None,
    ) -> None:
        if not isinstance(
            operation_persistence, AgentOperationPersistence
        ):
            raise TypeError(
                "operation_persistence must be an AgentOperationPersistence"
            )

        self._validate_persistence_contract(
            goal_task_persistence,
            "goal_task_persistence",
        )
        self._validate_persistence_contract(
            workflow_persistence,
            "workflow_persistence",
        )

        if operation_coordinator is None:
            operation_coordinator = AgentOperationCoordinator()

        if not isinstance(
            operation_coordinator,
            AgentOperationCoordinator,
        ):
            raise TypeError(
                "operation_coordinator must be an AgentOperationCoordinator"
            )

        self._operation_persistence = operation_persistence
        self._goal_task_persistence = goal_task_persistence
        self._workflow_persistence = workflow_persistence
        self._operation_coordinator = operation_coordinator

    @staticmethod
    def _validate_persistence_contract(
        persistence: object,
        name: str,
    ) -> None:
        if not callable(getattr(persistence, "load", None)):
            raise TypeError(f"{name} must provide a load method")

        if not callable(getattr(persistence, "save", None)):
            raise TypeError(f"{name} must provide a save method")

    def restore(
        self,
        operation_id: str,
        agent_id: str,
    ) -> tuple[
        AgentOperation,
        Goal,
        Workflow,
        tuple[WorkflowStep, ...],
        tuple[AgentTask, ...],
    ]:
        """Load and validate state without executing or resuming the operation."""
        if not isinstance(agent_id, str):
            raise TypeError("agent_id must be a string")

        if not agent_id.strip():
            raise ValueError("agent_id must not be empty")

        checkpoint = self._operation_persistence.load(operation_id)
        operation = checkpoint.operation

        goal_task_state: GoalTaskPersistenceState = (
            self._goal_task_persistence.load(agent_id)
        )
        workflow_state: WorkflowPersistenceState = (
            self._workflow_persistence.load(operation.workflow_id)
        )

        if goal_task_state.agent_id != agent_id:
            raise ValueError(
                "persisted goal/task state does not match the supplied agent"
            )

        goal = self._find_goal(goal_task_state.goals, operation.goal_id)
        workflow = workflow_state.workflow
        steps = workflow_state.steps
        tasks = goal_task_state.tasks

        self._operation_coordinator.validate(operation, goal, workflow)
        self._validate_step_tasks(steps, tasks, goal.id)
        self._validate_lifecycle(operation, workflow, steps, tasks)

        return operation, goal, workflow, steps, tasks

    @staticmethod
    def _find_goal(
        goals: tuple[Goal, ...],
        goal_id: str,
    ) -> Goal:
        for goal in goals:
            if goal.id == goal_id:
                return goal

        raise ValueError(f"persisted goal not found: {goal_id}")

    @staticmethod
    def _validate_step_tasks(
        steps: tuple[WorkflowStep, ...],
        tasks: tuple[AgentTask, ...],
        goal_id: str,
    ) -> None:
        tasks_by_id = {task.id: task for task in tasks}

        for step in steps:
            task = tasks_by_id.get(step.task_id)

            if task is None:
                raise ValueError(
                    f"workflow step references unknown task: {step.task_id}"
                )

            if task.goal_id != goal_id:
                raise ValueError(
                    f"workflow step task belongs to another goal: {task.id}"
                )

    @staticmethod
    def _validate_lifecycle(
        operation: AgentOperation,
        workflow: Workflow,
        steps: tuple[WorkflowStep, ...],
        tasks: tuple[AgentTask, ...],
    ) -> None:
        status = operation.status
        workflow_status = workflow.status

        if status is AgentOperationStatus.CREATED:
            if workflow_status not in {
                WorkflowStatus.READY,
                WorkflowStatus.RUNNING,
            }:
                raise ValueError(
                    "CREATED operation requires a READY or RUNNING workflow"
                )

        elif status in {
            AgentOperationStatus.RUNNING,
            AgentOperationStatus.PAUSED,
        }:
            if workflow_status is not WorkflowStatus.RUNNING:
                raise ValueError(
                    "active or paused operation requires a RUNNING workflow"
                )

        elif status is AgentOperationStatus.COMPLETED:
            if workflow_status is not WorkflowStatus.COMPLETED:
                raise ValueError(
                    "COMPLETED operation requires a COMPLETED workflow"
                )

        elif status is AgentOperationStatus.FAILED:
            if workflow_status is not WorkflowStatus.FAILED:
                raise ValueError(
                    "FAILED operation requires a FAILED workflow"
                )
            elif status is AgentOperationStatus.CANCELLED:
                # Cancellation leaves workflow and goal state unchanged.
                # Restoration validates the snapshot but never resumes it.
                pass

        if status in {
            AgentOperationStatus.RUNNING,
            AgentOperationStatus.PAUSED,
        }:
            if any(
                step.status is WorkflowStepStatus.RUNNING
                for step in steps
            ):
                raise ValueError(
                    "operation contains an interrupted RUNNING step; "
                    "automatic continuation is unsafe"
                )

        tasks_by_id = {task.id: task for task in tasks}

        for step in steps:
            task = tasks_by_id[step.task_id]

            if (
                step.status is WorkflowStepStatus.COMPLETED
                and task.status.value != "completed"
            ):
                raise ValueError(
                    f"completed step has a non-completed task: {task.id}"
                )

            if (
                step.status is WorkflowStepStatus.FAILED
                and task.status.value != "failed"
            ):
                raise ValueError(
                    f"failed step has a non-failed task: {task.id}"
                )
