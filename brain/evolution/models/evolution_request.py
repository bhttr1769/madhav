from dataclasses import dataclass

from brain.evolution.models.evolution_dependency_requirement import (
    EvolutionDependencyRequirement,
)


@dataclass(frozen=True)
class EvolutionRequest:
    requested_capability: str

    objective: str

    constraints: frozenset[str]

    mode: str

    dependency_requirements: tuple[
        EvolutionDependencyRequirement,
        ...,
    ] = ()