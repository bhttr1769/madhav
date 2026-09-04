from dataclasses import dataclass

from brain.code.models.code_structure import (
    CodeStructure,
)

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
class EngineeringGenerationRequest:
    """
    Represents the complete engineering context required for
    integrated code generation and engineering optimization.
    """

    task: Task

    design: SystemDesign

    plan: EngineeringPlan

    existing_code: CodeStructure