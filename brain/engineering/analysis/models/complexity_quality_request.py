from dataclasses import dataclass

from brain.code.models.code_structure import (
    CodeStructure,
)

from brain.engineering.design.models.system_design import (
    SystemDesign,
)

from brain.engineering.generation.models.engineering_decision import (
    EngineeringDecision,
)

from brain.engineering.generation.models.code_change import (
    CodeChange,
)

from brain.engineering.planning.models.plan import (
    EngineeringPlan,
)

from brain.engineering.tasks.models.task import (
    Task,
)


@dataclass(frozen=True)
class ComplexityQualityRequest:
    """
    Represents the complete engineering context required to analyze
    the complexity and implementation quality of a proposed change.
    """

    task: Task

    design: SystemDesign

    plan: EngineeringPlan

    engineering_decision: EngineeringDecision

    existing_code: CodeStructure

    proposed_changes: tuple[CodeChange, ...]