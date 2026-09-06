from dataclasses import dataclass

from brain.engineering.generation.models.code_change import CodeChange


@dataclass(frozen=True)
class RefactoringResult:
    changes: tuple[CodeChange, ...]
    rationale: str