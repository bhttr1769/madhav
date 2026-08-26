from dataclasses import dataclass


@dataclass(frozen=True)
class Context:
    """
    Represents unified information available to reasoning.
    """

    observations: frozenset[str]

    facts: frozenset[str]

    constraints: frozenset[str]

    goals: frozenset[str]