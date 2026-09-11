from dataclasses import dataclass


@dataclass(frozen=True)
class EvolutionPlan:
    requested_capability: str
    objective: str
    current_status: str
    reusable_capabilities: frozenset[str]
    required_capabilities: frozenset[str]
    tasks: tuple[str, ...]
    risks: frozenset[str]
    validation_strategy: tuple[str, ...]