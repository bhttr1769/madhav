from dataclasses import dataclass

from brain.agents.models.workflow import Workflow
from brain.agents.models.workflow_step import WorkflowStep


@dataclass(frozen=True)
class WorkflowPersistenceState:
    workflow: Workflow
    steps: tuple[WorkflowStep, ...]

    def __post_init__(self) -> None:
        if not isinstance(
            self.workflow,
            Workflow,
        ):
            raise TypeError(
                "workflow must be a Workflow"
            )

        if not isinstance(
            self.steps,
            tuple,
        ):
            raise TypeError(
                "steps must be a tuple"
            )

        for step in self.steps:
            if not isinstance(
                step,
                WorkflowStep,
            ):
                raise TypeError(
                    "steps must contain WorkflowStep instances"
                )

        step_ids = [
            step.id
            for step in self.steps
        ]

        if len(step_ids) != len(set(step_ids)):
            raise ValueError(
                "workflow persistence steps must have unique IDs"
            )

        if set(step_ids) != set(self.workflow.step_ids):
            raise ValueError(
                "persisted steps do not match workflow step IDs"
            )