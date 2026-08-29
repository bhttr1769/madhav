from dataclasses import dataclass


@dataclass(frozen=True)
class Task:
    """
    Represents an actionable engineering task.
    """

    id: str

    description: str

    category: str

    dependencies: frozenset[str]

    affected_areas: frozenset[str]

    acceptance_criteria: frozenset[str]