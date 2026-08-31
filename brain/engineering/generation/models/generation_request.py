from dataclasses import dataclass

from brain.engineering.design.models.system_design import (
    SystemDesign,
)

from brain.engineering.planning.models.plan import (
    EngineeringPlan,
)

from brain.engineering.tasks.models.task import (
    Task,
)


@dataclass(frozen=True)
class GenerationRequest:
    """
    Represents the engineering context required to generate
    an implementation for a specific engineering task.
    """

    task: Task

    design: SystemDesign

    plan: EngineeringPlan