from dataclasses import dataclass

from brain.engineering.generation.models.code_change import CodeChange


@dataclass(frozen=True)
class EngineeringLoopIteration:
    iteration: int
    changes: tuple[CodeChange, ...]
    passed: bool
    summary: str