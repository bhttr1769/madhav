from dataclasses import dataclass

from brain.code.models.code_structure import CodeStructure
from brain.engineering.analysis.models.engineering_quality_assessment import (
    EngineeringQualityAssessment,
)
from brain.engineering.design.models.system_design import SystemDesign
from brain.engineering.generation.models.code_change import CodeChange
from brain.engineering.generation.models.engineering_decision import (
    EngineeringDecision,
)
from brain.engineering.planning.models.plan import EngineeringPlan
from brain.engineering.tasks.models.task import Task


@dataclass(frozen=True)
class OptimizationDecisionRequest:
    """
    Represents the complete engineering context required to determine
    whether and how a proposed implementation should be optimized.
    """

    task: Task
    design: SystemDesign
    plan: EngineeringPlan
    engineering_decision: EngineeringDecision
    quality_assessment: EngineeringQualityAssessment
    existing_code: CodeStructure
    proposed_changes: tuple[CodeChange, ...]