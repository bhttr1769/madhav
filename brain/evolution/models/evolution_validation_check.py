from dataclasses import dataclass


@dataclass(frozen=True)
class EvolutionValidationCheck:
    name: str
    passed: bool
    reason: str