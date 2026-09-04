from dataclasses import dataclass

from brain.code.models.code_structure import (
    CodeStructure,
)

from brain.engineering.analysis.models.engineering_quality_assessment import (
    EngineeringQualityAssessment,
)

from brain.engineering.design.models.system_design import (
    SystemDesign,
)

from brain.engineering.generation.models.code_change import (
    CodeChange,
)

from brain.engineering.generation.models.engineering_decision import (
    EngineeringDecision,
)

from brain.engineering.optimization.models.optimization_decision import (
    OptimizationDecision,
)

from brain.engineering.planning.models.plan import (
    EngineeringPlan,
)

from brain.engineering.tasks.models.task import (
    Task,
)


@dataclass(frozen=True)
class FinalGenerationRequest:
    """
    Represents the complete engineering context required to produce
    the final implementation after engineering analysis.
    """

    task: Task

    design: SystemDesign

    plan: EngineeringPlan

    existing_code: CodeStructure

    engineering_decision: EngineeringDecision

    quality_assessment: EngineeringQualityAssessment

    optimization_decision: OptimizationDecision

    proposed_changes: tuple[CodeChange, ...]