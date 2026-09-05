from dataclasses import dataclass

from brain.code.models.code_structure import CodeStructure
from brain.engineering.design.models.system_design import SystemDesign
from brain.engineering.generation.models.engineering_decision import EngineeringDecision
from brain.engineering.planning.models.plan import EngineeringPlan
from brain.engineering.tasks.models.task import Task


@dataclass(frozen=True)
class GenerationRequest:
    """
    Represents the engineering context required to generate
    a candidate implementation for a specific engineering task.
    """

    task: Task
    design: SystemDesign
    plan: EngineeringPlan
    existing_code: CodeStructure
    engineering_decision: EngineeringDecision