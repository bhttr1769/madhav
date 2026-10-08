from dataclasses import replace

from brain.agents.models.agent_task import AgentTask
from brain.agents.models.workflow import Workflow, WorkflowStatus
from brain.agents.models.workflow_step import (
    WorkflowStep,
    WorkflowStepStatus,
)
from brain.agents.workflow_lifecycle import WorkflowLifecycle
from brain.agents.workflow_task_integration import WorkflowTaskIntegration


class WorkflowCoordinator:
    def __init__(
        self,
        task_integration: WorkflowTaskIntegration | None = None,
    ) -> None:
        if task_integration is None:
            task_integration = WorkflowTaskIntegration()

        if not isinstance(
            task_integration,
            WorkflowTaskIntegration,
        ):
            raise TypeError(
                "task_integration must be a WorkflowTaskIntegration"
            )

        self._task_integration = task_integration

    def start(
        self,
        workflow: Workflow,
        steps: tuple[WorkflowStep, ...],
        tasks: tuple[AgentTask, ...] | None = None,
    ) -> tuple[Workflow, tuple[WorkflowStep, ...]]:
        self._validate_workflow_steps(
            workflow,
            steps,
        )

        if tasks is not None:
            self._task_integration.validate(
                workflow,
                steps,
                tasks,
            )

            ready_steps = self._task_integration.ready_steps(
                workflow,
                steps,
                tasks,
            )

            ready_step_ids = {
                step.id
                for step in ready_steps
            }
        else:
            ready_step_ids = {
                step.id
                for step in steps
            }

        WorkflowLifecycle.validate_workflow_transition(
            workflow.status,
            WorkflowStatus.READY,
        )

        workflow = replace(
            workflow,
            status=WorkflowStatus.READY,
        )

        WorkflowLifecycle.validate_workflow_transition(
            workflow.status,
            WorkflowStatus.RUNNING,
        )

        workflow = replace(
            workflow,
            status=WorkflowStatus.RUNNING,
        )

        updated_steps = tuple(
            replace(
                step,
                status=WorkflowStepStatus.READY,
            )
            if (
                step.status is WorkflowStepStatus.PENDING
                and step.id in ready_step_ids
            )
            else step
            for step in steps
        )

        return workflow, updated_steps

    def refresh_ready_steps(
        self,
        workflow: Workflow,
        steps: tuple[WorkflowStep, ...],
        tasks: tuple[AgentTask, ...],
    ) -> tuple[WorkflowStep, ...]:
        self._validate_workflow_steps(
            workflow,
            steps,
        )

        self._task_integration.validate(
            workflow,
            steps,
            tasks,
        )

        ready_steps = self._task_integration.ready_steps(
            workflow,
            steps,
            tasks,
        )

        ready_step_ids = {
            step.id
            for step in ready_steps
        }

        return tuple(
            replace(
                step,
                status=WorkflowStepStatus.READY,
            )
            if (
                step.status is WorkflowStepStatus.PENDING
                and step.id in ready_step_ids
            )
            else step
            for step in steps
        )

    def start_step(
        self,
        workflow: Workflow,
        steps: tuple[WorkflowStep, ...],
        step_id: str,
    ) -> tuple[Workflow, tuple[WorkflowStep, ...]]:
        self._validate_workflow_steps(
            workflow,
            steps,
        )

        self._validate_step_id(step_id)

        if workflow.status is not WorkflowStatus.RUNNING:
            raise ValueError(
                "workflow must be RUNNING to start a step"
            )

        step = self._find_step(
            steps,
            step_id,
        )

        WorkflowLifecycle.validate_step_transition(
            step.status,
            WorkflowStepStatus.RUNNING,
        )

        updated_steps = tuple(
            replace(
                current,
                status=WorkflowStepStatus.RUNNING,
            )
            if current.id == step_id
            else current
            for current in steps
        )

        return workflow, updated_steps

    def complete_step(
        self,
        workflow: Workflow,
        steps: tuple[WorkflowStep, ...],
        step_id: str,
    ) -> tuple[Workflow, tuple[WorkflowStep, ...]]:
        self._validate_workflow_steps(
            workflow,
            steps,
        )

        self._validate_step_id(step_id)

        step = self._find_step(
            steps,
            step_id,
        )

        WorkflowLifecycle.validate_step_transition(
            step.status,
            WorkflowStepStatus.COMPLETED,
        )

        updated_steps = tuple(
            replace(
                current,
                status=WorkflowStepStatus.COMPLETED,
            )
            if current.id == step_id
            else current
            for current in steps
        )

        if all(
            current.status is WorkflowStepStatus.COMPLETED
            for current in updated_steps
        ):
            WorkflowLifecycle.validate_workflow_transition(
                workflow.status,
                WorkflowStatus.COMPLETED,
            )

            workflow = replace(
                workflow,
                status=WorkflowStatus.COMPLETED,
            )

        return workflow, updated_steps

    def fail_step(
        self,
        workflow: Workflow,
        steps: tuple[WorkflowStep, ...],
        step_id: str,
    ) -> tuple[Workflow, tuple[WorkflowStep, ...]]:
        self._validate_workflow_steps(
            workflow,
            steps,
        )

        self._validate_step_id(step_id)

        step = self._find_step(
            steps,
            step_id,
        )

        WorkflowLifecycle.validate_step_transition(
            step.status,
            WorkflowStepStatus.FAILED,
        )

        updated_steps = tuple(
            replace(
                current,
                status=WorkflowStepStatus.FAILED,
            )
            if current.id == step_id
            else current
            for current in steps
        )

        WorkflowLifecycle.validate_workflow_transition(
            workflow.status,
            WorkflowStatus.FAILED,
        )

        workflow = replace(
            workflow,
            status=WorkflowStatus.FAILED,
        )

        return workflow, updated_steps

    @staticmethod
    def _validate_step_id(step_id: str) -> None:
        if not isinstance(step_id, str):
            raise TypeError(
                "step_id must be a string"
            )

        if not step_id.strip():
            raise ValueError(
                "step_id must not be empty"
            )

    @staticmethod
    def _find_step(
        steps: tuple[WorkflowStep, ...],
        step_id: str,
    ) -> WorkflowStep:
        for step in steps:
            if step.id == step_id:
                return step

        raise ValueError(
            f"Workflow step not found: {step_id}"
        )

    @staticmethod
    def _validate_workflow_steps(
        workflow: Workflow,
        steps: tuple[WorkflowStep, ...],
    ) -> None:
        if not isinstance(
            workflow,
            Workflow,
        ):
            raise TypeError(
                "workflow must be a Workflow"
            )

        if not isinstance(
            steps,
            tuple,
        ):
            raise TypeError(
                "steps must be a tuple"
            )

        for step in steps:
            if not isinstance(
                step,
                WorkflowStep,
            ):
                raise TypeError(
                    "all steps must be WorkflowStep instances"
                )

        step_ids = [
            step.id
            for step in steps
        ]

        if len(step_ids) != len(set(step_ids)):
            raise ValueError(
                "duplicate workflow step IDs are not allowed"
            )

        if set(step_ids) != set(workflow.step_ids):
            raise ValueError(
                "provided steps do not match workflow step IDs"
            )