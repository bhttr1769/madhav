from dataclasses import dataclass

from brain.engineering.design.models.system_design import (
    SystemDesign,
)
from brain.engineering.planning.models.plan import (
    EngineeringPlan,
)
from brain.engineering.requirements.models.requirement import (
    Requirement,
)
from brain.engineering.tasks.models.task_decomposition import (
    TaskDecomposition,
)


@dataclass(frozen=True)
class EvolutionProposal:
    requested_capability: str
    requirement: Requirement
    task_decomposition: TaskDecomposition
    design: SystemDesign
    plan: EngineeringPlan