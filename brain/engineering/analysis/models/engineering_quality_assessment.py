from dataclasses import dataclass


@dataclass(frozen=True)
class EngineeringQualityAssessment:
    """
    Represents the assessed complexity and implementation quality
    of a proposed engineering change.
    """

    complexity: str

    structural_complexity: str

    cognitive_complexity: str

    algorithmic_complexity: str

    dependency_complexity: str

    abstraction_complexity: str

    maintainability: str

    clarity: str

    cohesion: str

    coupling: str

    testability: str

    extensibility: str

    over_engineering: bool

    issues: tuple[str, ...]

    strengths: tuple[str, ...]

    recommendations: tuple[str, ...]

    rationale: tuple[str, ...]