from dataclasses import dataclass

from brain.engineering.generation.models.code_change import (
    CodeChange,
)
from brain.engineering.loop.models.engineering_loop_result import (
    EngineeringLoopResult,
)
from brain.engineering.planning.models.plan import (
    EngineeringPlan,
)
from brain.engineering.design.models.system_design import (
    SystemDesign,
)
from brain.engineering.requirements.models.requirement import (
    Requirement,
)
from brain.engineering.tasks.models.task_decomposition import (
    TaskDecomposition,
)


@dataclass(frozen=True)
class EvolutionResult:
    requested_capability: str
    requirement: Requirement
    task_decomposition: TaskDecomposition
    design: SystemDesign
    plan: EngineeringPlan
    proposed_changes: tuple[CodeChange, ...]
    engineering_result: EngineeringLoopResult