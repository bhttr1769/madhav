from brain.agents.models.workflow import WorkflowStatus
from brain.agents.models.workflow_step import WorkflowStepStatus


class WorkflowLifecycle:
    """
    Validates lifecycle transitions for workflows and workflow steps.

    This component does not mutate workflow or workflow-step objects.
    It only determines whether a requested transition is valid.
    """

    _WORKFLOW_TRANSITIONS: dict[
        WorkflowStatus,
        frozenset[WorkflowStatus],
    ] = {
        WorkflowStatus.CREATED: frozenset({
            WorkflowStatus.READY,
        }),
        WorkflowStatus.READY: frozenset({
            WorkflowStatus.RUNNING,
        }),
        WorkflowStatus.RUNNING: frozenset({
            WorkflowStatus.COMPLETED,
            WorkflowStatus.FAILED,
        }),
        WorkflowStatus.COMPLETED: frozenset(),
        WorkflowStatus.FAILED: frozenset(),
    }

    _STEP_TRANSITIONS: dict[
        WorkflowStepStatus,
        frozenset[WorkflowStepStatus],
    ] = {
        WorkflowStepStatus.PENDING: frozenset({
            WorkflowStepStatus.READY,
        }),
        WorkflowStepStatus.READY: frozenset({
            WorkflowStepStatus.RUNNING,
        }),
        WorkflowStepStatus.RUNNING: frozenset({
            WorkflowStepStatus.COMPLETED,
            WorkflowStepStatus.FAILED,
        }),
        WorkflowStepStatus.COMPLETED: frozenset(),
        WorkflowStepStatus.FAILED: frozenset(),
    }

    @classmethod
    def can_transition_workflow(
        cls,
        current: WorkflowStatus,
        target: WorkflowStatus,
    ) -> bool:
        cls._validate_workflow_status(current)
        cls._validate_workflow_status(target)

        return target in cls._WORKFLOW_TRANSITIONS[current]

    @classmethod
    def validate_workflow_transition(
        cls,
        current: WorkflowStatus,
        target: WorkflowStatus,
    ) -> None:
        if not cls.can_transition_workflow(
            current,
            target,
        ):
            raise ValueError(
                f"Invalid workflow transition: "
                f"{current.value} -> {target.value}"
            )

    @classmethod
    def can_transition_step(
        cls,
        current: WorkflowStepStatus,
        target: WorkflowStepStatus,
    ) -> bool:
        cls._validate_step_status(current)
        cls._validate_step_status(target)

        return target in cls._STEP_TRANSITIONS[current]

    @classmethod
    def validate_step_transition(
        cls,
        current: WorkflowStepStatus,
        target: WorkflowStepStatus,
    ) -> None:
        if not cls.can_transition_step(
            current,
            target,
        ):
            raise ValueError(
                f"Invalid workflow step transition: "
                f"{current.value} -> {target.value}"
            )

    @staticmethod
    def _validate_workflow_status(
        status: WorkflowStatus,
    ) -> None:
        if not isinstance(status, WorkflowStatus):
            raise TypeError(
                "status must be a WorkflowStatus"
            )

    @staticmethod
    def _validate_step_status(
        status: WorkflowStepStatus,
    ) -> None:
        if not isinstance(status, WorkflowStepStatus):
            raise TypeError(
                "status must be a WorkflowStepStatus"
            )