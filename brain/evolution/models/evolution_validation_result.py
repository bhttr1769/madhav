from dataclasses import dataclass

from brain.evolution.models.evolution_validation_check import (
    EvolutionValidationCheck,
)


@dataclass(frozen=True)
class EvolutionValidationResult:
    checks: tuple[EvolutionValidationCheck, ...]

    @property
    def passed(self) -> bool:
        return all(
            check.passed
            for check in self.checks
        )