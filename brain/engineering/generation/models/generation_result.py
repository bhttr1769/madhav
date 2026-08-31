from dataclasses import dataclass

from brain.engineering.generation.models.code_change import (
    CodeChange,
)

from brain.engineering.generation.models.engineering_decision import (
    EngineeringDecision,
)


@dataclass(frozen=True)
class GenerationResult:
    """
    Represents generated code together with the engineering
    decision behind the implementation.
    """

    changes: tuple[CodeChange, ...]

    decision: EngineeringDecision