from enum import Enum


class EvolutionDependencySafetyStatus(
    Enum,
):
    """
    Represents whether dependency plans are safe
    to proceed with during evolution.
    """

    ALLOWED = "allowed"

    BLOCKED = "blocked"