from dataclasses import dataclass

from brain.engineering.generation.models.code_change import (
    CodeChange,
)


@dataclass(frozen=True)
class TestGenerationResult:
    """
    Represents generated test changes.
    """

    changes: tuple[CodeChange, ...]