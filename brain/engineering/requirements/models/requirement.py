from dataclasses import dataclass


@dataclass(frozen=True)
class Requirement:
    """
    Structured understanding of an engineering request.
    """

    original_request: str

    objective: str

    functional_requirements: frozenset[str]

    non_functional_requirements: frozenset[str]

    constraints: frozenset[str]

    acceptance_criteria: frozenset[str]

    assumptions: frozenset[str]

    ambiguities: frozenset[str]

    affected_areas: frozenset[str]

    confidence: float