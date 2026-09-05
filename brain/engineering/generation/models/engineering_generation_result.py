from dataclasses import dataclass

from brain.engineering.analysis.models.engineering_quality_assessment import (
    EngineeringQualityAssessment,
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


@dataclass(frozen=True)
class EngineeringGenerationResult:
    """
    Represents the result of integrated engineering analysis,
    optimization, and code generation.

    Quality assessment and optimization decision are absent when
    implementation is not required.
    """

    changes: tuple[CodeChange, ...]
    engineering_decision: EngineeringDecision
    quality_assessment: EngineeringQualityAssessment | None
    optimization_decision: OptimizationDecision | None