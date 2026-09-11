from dataclasses import dataclass


@dataclass(frozen=True)
class EvolutionRequest:
    requested_capability: str

    objective: str

    constraints: frozenset[str]

    mode: str