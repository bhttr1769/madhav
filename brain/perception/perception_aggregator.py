from brain.perception.models.observation import (
    Observation,
)


class PerceptionAggregator:
    """
    Aggregates observations from multiple
    perception subsystems.
    """

    def aggregate(
        self,
        observations: list[Observation],
    ) -> frozenset[Observation]:

        return frozenset(
            observations
        )