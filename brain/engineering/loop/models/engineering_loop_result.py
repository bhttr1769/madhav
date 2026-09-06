from dataclasses import dataclass

from brain.engineering.generation.models.code_change import CodeChange
from brain.engineering.loop.models.engineering_loop_iteration import (
    EngineeringLoopIteration,
)


@dataclass(frozen=True)
class EngineeringLoopResult:
    changes: tuple[CodeChange, ...]
    passed: bool
    iterations: tuple[EngineeringLoopIteration, ...]
    termination_reason: str