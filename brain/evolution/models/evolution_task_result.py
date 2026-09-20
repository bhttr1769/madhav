from dataclasses import dataclass

from brain.engineering.generation.models.code_change import (
    CodeChange,
)
from brain.engineering.loop.models.engineering_loop_result import (
    EngineeringLoopResult,
)


@dataclass(frozen=True)
class EvolutionTaskResult:
    task_id: str
    task_description: str
    proposed_changes: tuple[CodeChange, ...]
    engineering_result: EngineeringLoopResult