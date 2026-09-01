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
class NecessityReuseRequest:
    """
    Represents the engineering context required for necessity
    and reuse analysis.
    """

    task: Task

    design: SystemDesign

    plan: EngineeringPlan

    existing_code: CodeStructure


AnalysisRequest = NecessityReuseRequest