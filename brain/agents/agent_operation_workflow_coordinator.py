
from dataclasses import replace

from brain.agents.agent_operation_coordinator import (
    AgentOperationCoordinator,
)
from brain.agents.agent_runtime import AgentRuntime
from brain.agents.agent_task_lifecycle import AgentTaskLifecycle
from brain.agents.goal_task_persistence import GoalTaskPersistence
from brain.agents.models.agent_operation import (
    AgentOperation,
    AgentOperationStatus,
)
from brain.agents.models.agent_operation_checkpoint_state import (
    AgentOperationCheckpointState,
)
from brain.agents.models.agent_task import AgentTask
from brain.agents.models.agent_task_status import AgentTaskStatus
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
from brain.agents.workflow_coordinator import WorkflowCoordinator
from brain.agents.workflow_persistence import WorkflowPersistence


class AgentOperationWorkflowCoordinator:
    """Coordinates operation transitions and optionally persists their state."""

    def __init__(
        self,
        operation_coordinator: AgentOperationCoordinator | None = None,
        workflow_coordinator: WorkflowCoordinator | None = None,
        operation_persistence: AgentOperationPersistence | None = None,
        goal_task_persistence: GoalTaskPersistence | None = None,
        workflow_persistence: WorkflowPersistence | None = None,
    ) -> None:
        if operation_coordinator is None:
            operation_coordinator = AgentOperationCoordinator()

        if not isinstance(
            operation_coordinator,
            AgentOperationCoordinator,
        ):
            raise TypeError(
                "operation_coordinator must be an AgentOperationCoordinator"
            )

        if workflow_coordinator is None:
            workflow_coordinator = WorkflowCoordinator()

        if not isinstance(workflow_coordinator, WorkflowCoordinator):
            raise TypeError(
                "workflow_coordinator must be a WorkflowCoordinator"
            )

        persistence_dependencies = (
            operation_persistence,
            goal_task_persistence,
            workflow_persistence,
        )

        if any(item is not None for item in persistence_dependencies):
            if not all(item is not None for item in persistence_dependencies):
                raise ValueError(
                    "all three persistence dependencies must be provided together"
                )

            for item in persistence_dependencies:
                if not callable(getattr(item, "save", None)):
                    raise TypeError(
                        "persistence dependencies must provide save()"
                    )
                if not callable(getattr(item, "load", None)):
                    raise TypeError(
                        "persistence dependencies must provide load()"
                    )

        self._operation_coordinator = operation_coordinator
        self._workflow_coordinator = workflow_coordinator
        self._operation_persistence = operation_persistence
        self._goal_task_persistence = goal_task_persistence
        self._workflow_persistence = workflow_persistence

    def _save_operation(self, operation: AgentOperation) -> None:
        if self._operation_persistence is None:
            return

        self._operation_persistence.save(
            AgentOperationCheckpointState(operation=operation)
        )

    def _save_workflow(
        self,
        workflow: Workflow,
        steps: tuple[WorkflowStep, ...],
    ) -> None:
        if self._workflow_persistence is None:
            return

        self._workflow_persistence.save(
            WorkflowPersistenceState(
                workflow=workflow,
                steps=steps,
            )
        )

    def _save_goal_tasks(
        self,
        goal: Goal,
        tasks: tuple[AgentTask, ...],
    ) -> None:
        if self._goal_task_persistence is None:
            return

        try:
            existing = self._goal_task_persistence.load(goal.agent_id)
        except KeyError:
            existing = GoalTaskPersistenceState(
                agent_id=goal.agent_id,
                goals=(),
                tasks=(),
            )

        goals_by_id = {item.id: item for item in existing.goals}

        # Replace the task snapshot for this goal while preserving
        # tasks belonging to other goals owned by the same agent.
        tasks_by_id = {
            item.id: item
            for item in existing.tasks
            if item.goal_id != goal.id
        }

        goals_by_id[goal.id] = goal

        for task in tasks:
            if task.goal_id == goal.id:
                tasks_by_id[task.id] = task

        self._goal_task_persistence.save(
            GoalTaskPersistenceState(
                agent_id=goal.agent_id,
                goals=tuple(goals_by_id.values()),
                tasks=tuple(tasks_by_id.values()),
            )
        )

    def pause(
        self,
        operation: AgentOperation,
        goal: Goal,
        workflow: Workflow,
        steps: tuple[WorkflowStep, ...],
    ) -> AgentOperation:
        """Pause an operation only when no workflow step is running."""
        self._validate_context(operation, goal, workflow)
        self._require_running(operation)
        self._validate_steps(workflow, steps)

        if workflow.status is not WorkflowStatus.RUNNING:
            raise ValueError("workflow must be RUNNING to pause an operation")

        if any(
            step.status is WorkflowStepStatus.RUNNING
            for step in steps
        ):
            raise ValueError(
                "operation can only be paused when no workflow step is RUNNING"
            )

        updated_operation = self._operation_coordinator.pause(
            operation,
            goal,
            workflow,
        )
        self._save_operation(updated_operation)
        return updated_operation

    def resume(
        self,
        operation: AgentOperation,
        goal: Goal,
        workflow: Workflow,
    ) -> AgentOperation:
        """Resume an operation whose workflow is still running."""
        self._validate_context(operation, goal, workflow)

        if operation.status is not AgentOperationStatus.PAUSED:
            raise ValueError("operation must be PAUSED to resume")

        updated_operation = self._operation_coordinator.resume(
            operation,
            goal,
            workflow,
        )
        self._save_operation(updated_operation)
        return updated_operation

    def start_step(
        self,
        operation: AgentOperation,
        goal: Goal,
        workflow: Workflow,
        steps: tuple[WorkflowStep, ...],
        step_id: str,
    ) -> tuple[Workflow, tuple[WorkflowStep, ...]]:
        """Start a step only while its operation is running."""
        self._require_running_context(operation, goal, workflow)

        updated_workflow, updated_steps = (
            self._workflow_coordinator.start_step(
                workflow,
                steps,
                step_id,
            )
        )

        self._save_workflow(updated_workflow, updated_steps)
        return updated_workflow, updated_steps

    def refresh_ready_steps(
        self,
        operation: AgentOperation,
        goal: Goal,
        workflow: Workflow,
        steps: tuple[WorkflowStep, ...],
        tasks: tuple[AgentTask, ...],
    ) -> tuple[WorkflowStep, ...]:
        """Refresh eligible steps only while the operation is running."""
        self._require_running_context(operation, goal, workflow)

        updated_steps = self._workflow_coordinator.refresh_ready_steps(
            workflow,
            steps,
            tasks,
        )

        self._save_workflow(workflow, updated_steps)
        return updated_steps

    def complete_step(
        self,
        operation: AgentOperation,
        goal: Goal,
        workflow: Workflow,
        steps: tuple[WorkflowStep, ...],
        step_id: str,
    ) -> tuple[Workflow, tuple[WorkflowStep, ...]]:
        """Complete a step while its operation is running."""
        self._require_running_context(operation, goal, workflow)

        updated_workflow, updated_steps = (
            self._workflow_coordinator.complete_step(
                workflow,
                steps,
                step_id,
            )
        )

        self._save_workflow(updated_workflow, updated_steps)
        return updated_workflow, updated_steps

    def fail_step(
        self,
        operation: AgentOperation,
        goal: Goal,
        workflow: Workflow,
        steps: tuple[WorkflowStep, ...],
        step_id: str,
    ) -> tuple[AgentOperation, Workflow, tuple[WorkflowStep, ...]]:
        """Fail both the workflow and operation after a step failure."""
        self._require_running_context(operation, goal, workflow)

        updated_workflow, updated_steps = (
            self._workflow_coordinator.fail_step(
                workflow,
                steps,
                step_id,
            )
        )

        updated_operation = self._operation_coordinator.fail(
            operation,
            goal,
            updated_workflow,
        )

        self._save_workflow(updated_workflow, updated_steps)
        self._save_operation(updated_operation)

        return updated_operation, updated_workflow, updated_steps

    def start_task_step(
        self,
        operation: AgentOperation,
        runtime: AgentRuntime,
        goal: Goal,
        workflow: Workflow,
        steps: tuple[WorkflowStep, ...],
        tasks: tuple[AgentTask, ...],
        step_id: str,
    ) -> tuple[Workflow, tuple[WorkflowStep, ...], tuple[AgentTask, ...]]:
        """Authorize and start a workflow step with its associated task."""
        self._require_running_context(operation, goal, workflow)
        self._validate_steps(workflow, steps)
        self._validate_tasks(tasks)

        runtime.authorize_goal(goal)

        step = self._find_step(steps, step_id)
        task = self._find_task(tasks, step.task_id)

        runtime.authorize_task(task, goal)

        if task.goal_id != goal.id:
            raise ValueError("task does not belong to the supplied goal")

        AgentTaskLifecycle.transition(
            task.status,
            AgentTaskStatus.ACTIVE,
        )

        updated_workflow, updated_steps = (
            self._workflow_coordinator.start_step(
                workflow,
                steps,
                step_id,
            )
        )

        updated_task = replace(
            task,
            status=AgentTaskStatus.ACTIVE,
        )
        updated_tasks = self._replace_task(tasks, updated_task)

        self._save_workflow(updated_workflow, updated_steps)
        self._save_goal_tasks(goal, updated_tasks)

        return updated_workflow, updated_steps, updated_tasks

    def complete_task_step(
        self,
        operation: AgentOperation,
        runtime: AgentRuntime,
        goal: Goal,
        workflow: Workflow,
        steps: tuple[WorkflowStep, ...],
        tasks: tuple[AgentTask, ...],
        step_id: str,
    ) -> tuple[
        AgentOperation,
        Workflow,
        tuple[WorkflowStep, ...],
        tuple[AgentTask, ...],
    ]:
        """Complete a workflow step and synchronize its task and operation."""
        self._require_running_context(operation, goal, workflow)
        self._validate_steps(workflow, steps)
        self._validate_tasks(tasks)

        runtime.authorize_goal(goal)

        step = self._find_step(steps, step_id)
        task = self._find_task(tasks, step.task_id)

        runtime.authorize_task(task, goal)

        if task.goal_id != goal.id:
            raise ValueError("task does not belong to the supplied goal")

        AgentTaskLifecycle.transition(
            task.status,
            AgentTaskStatus.COMPLETED,
        )

        updated_workflow, updated_steps = (
            self._workflow_coordinator.complete_step(
                workflow,
                steps,
                step_id,
            )
        )

        updated_task = replace(
            task,
            status=AgentTaskStatus.COMPLETED,
            progress=100,
        )
        updated_tasks = self._replace_task(tasks, updated_task)

        updated_operation = operation
        if updated_workflow.status is WorkflowStatus.COMPLETED:
            updated_operation = self._operation_coordinator.complete(
                operation,
                goal,
                updated_workflow,
            )

        self._save_workflow(updated_workflow, updated_steps)
        self._save_goal_tasks(goal, updated_tasks)

        if updated_operation is not operation:
            self._save_operation(updated_operation)

        return (
            updated_operation,
            updated_workflow,
            updated_steps,
            updated_tasks,
        )

    def fail_task_step(
        self,
        operation: AgentOperation,
        runtime: AgentRuntime,
        goal: Goal,
        workflow: Workflow,
        steps: tuple[WorkflowStep, ...],
        tasks: tuple[AgentTask, ...],
        step_id: str,
    ) -> tuple[
        AgentOperation,
        Workflow,
        tuple[WorkflowStep, ...],
        tuple[AgentTask, ...],
    ]:
        """Fail a step and persist its related state in order."""
        self._require_running_context(operation, goal, workflow)
        self._validate_steps(workflow, steps)
        self._validate_tasks(tasks)

        runtime.authorize_goal(goal)

        step = self._find_step(steps, step_id)
        task = self._find_task(tasks, step.task_id)

        runtime.authorize_task(task, goal)

        if task.goal_id != goal.id:
            raise ValueError("task does not belong to the supplied goal")

        AgentTaskLifecycle.transition(
            task.status,
            AgentTaskStatus.FAILED,
        )

        updated_workflow, updated_steps = (
            self._workflow_coordinator.fail_step(
                workflow,
                steps,
                step_id,
            )
        )

        updated_operation = self._operation_coordinator.fail(
            operation,
            goal,
            updated_workflow,
        )

        updated_task = replace(
            task,
            status=AgentTaskStatus.FAILED,
        )
        updated_tasks = self._replace_task(tasks, updated_task)

        self._save_workflow(updated_workflow, updated_steps)
        self._save_goal_tasks(goal, updated_tasks)
        self._save_operation(updated_operation)

        return (
            updated_operation,
            updated_workflow,
            updated_steps,
            updated_tasks,
        )

    def _require_running_context(
        self,
        operation: AgentOperation,
        goal: Goal,
        workflow: Workflow,
    ) -> None:
        self._validate_context(operation, goal, workflow)
        self._require_running(operation)

    def _validate_context(
        self,
        operation: AgentOperation,
        goal: Goal,
        workflow: Workflow,
    ) -> None:
        self._operation_coordinator.validate(
            operation,
            goal,
            workflow,
        )

    @staticmethod
    def _require_running(operation: AgentOperation) -> None:
        if operation.status is not AgentOperationStatus.RUNNING:
            raise ValueError("operation must be RUNNING to advance its workflow")

    @staticmethod
    def _validate_steps(
        workflow: Workflow,
        steps: tuple[WorkflowStep, ...],
    ) -> None:
        if not isinstance(steps, tuple):
            raise TypeError("steps must be a tuple")

        if any(not isinstance(step, WorkflowStep) for step in steps):
            raise TypeError("all steps must be WorkflowStep instances")

        step_ids = tuple(step.id for step in steps)

        if len(step_ids) != len(set(step_ids)):
            raise ValueError("duplicate workflow step IDs are not allowed")

        if set(step_ids) != set(workflow.step_ids):
            raise ValueError(
                "provided steps do not match workflow step IDs"
            )

    @staticmethod
    def _validate_tasks(tasks: tuple[AgentTask, ...]) -> None:
        if not isinstance(tasks, tuple):
            raise TypeError("tasks must be a tuple")

        if any(not isinstance(task, AgentTask) for task in tasks):
            raise TypeError("all tasks must be AgentTask instances")

        task_ids = tuple(task.id for task in tasks)
        if len(task_ids) != len(set(task_ids)):
            raise ValueError("duplicate task IDs are not allowed")

    @staticmethod
    def _find_step(
        steps: tuple[WorkflowStep, ...],
        step_id: str,
    ) -> WorkflowStep:
        for step in steps:
            if step.id == step_id:
                return step

        raise ValueError(f"workflow step not found: {step_id}")

    @staticmethod
    def _find_task(
        tasks: tuple[AgentTask, ...],
        task_id: str,
    ) -> AgentTask:
        for task in tasks:
            if task.id == task_id:
                return task

        raise ValueError(f"task not found for workflow step: {task_id}")

    @staticmethod
    def _replace_task(
        tasks: tuple[AgentTask, ...],
        updated_task: AgentTask,
    ) -> tuple[AgentTask, ...]:
        return tuple(
            updated_task if task.id == updated_task.id else task
            for task in tasks
        )
