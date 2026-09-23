from enum import Enum


class EvolutionDependencyPlanOperation(
    Enum,
):
    """
    Represents the dependency operation proposed by
    an evolution dependency plan.
    """

    NO_ACTION = "no_action"

    ADD = "add"

    UPDATE = "update"

    BLOCKED = "blocked"