from dataclasses import dataclass


@dataclass(frozen=True)
class EngineeringPlan:
    """
    Structured engineering plan derived from a task decomposition.
    """

    task_order: tuple[str, ...]

    strategy: tuple[str, ...]

    milestones: tuple[str, ...]

    required_capabilities: frozenset[str]

    risks: frozenset[str]

    assumptions: frozenset[str]

    validation_strategy: tuple[str, ...]

    confidence: float