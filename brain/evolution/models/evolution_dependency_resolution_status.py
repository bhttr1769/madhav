from enum import Enum


class EvolutionDependencyResolutionStatus(
    Enum,
):
    """
    Represents the resolution state of an
    evolution dependency.
    """

    NOT_REQUIRED = "not_required"

    RESOLVABLE = "resolvable"

    NOT_RESOLVABLE = "not_resolvable"

    UNRESOLVED = "unresolved"