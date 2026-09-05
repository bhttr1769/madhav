from dataclasses import dataclass


@dataclass(frozen=True)
class EngineeringDecision:
    """
    Represents the engineering judgment behind a proposed implementation.
    """

    implementation_required: bool

    necessity: str

    reuse_existing: bool

    use_standard_library: bool

    use_existing_dependency: bool

    new_dependency_required: bool

    abstraction_justified: bool

    optimization_justified: bool

    rationale: tuple[str, ...]