from enum import Enum


class EvolutionDependencyStatus(
    Enum,
):
    """
    Represents the availability state of an evolution dependency.
    """

    AVAILABLE = "available"

    MISSING = "missing"

    VERSION_MISMATCH = (
        "version_mismatch"
    )

    UNRESOLVED = "unresolved"