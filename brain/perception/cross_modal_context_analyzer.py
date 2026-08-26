from brain.perception.models.cross_modal_context import (
    CrossModalContext,
)

from brain.perception.models.observation import (
    Observation,
)


class CrossModalContextAnalyzer:
    """
    Finds explicit relationships between observations
    from different perception sources.
    """

    def analyze(
        self,
        observations: frozenset[Observation],
    ) -> CrossModalContext:

        relationships = set()

        ordered = sorted(
            observations,
            key=self._observation_key,
        )

        for index, left in enumerate(ordered):

            for right in ordered[index + 1:]:

                relationship = (
                    self._infer_relationship(
                        left,
                        right,
                    )
                )

                if relationship is None:
                    continue

                relationships.add(
                    relationship
                )

        return CrossModalContext(
            observations=observations,
            relationships=frozenset(
                relationships
            ),
        )

    def _infer_relationship(
        self,
        left: Observation,
        right: Observation,
    ) -> tuple[str, str, str] | None:

        if left.source == right.source:
            return None

        if (
            left.category == "technology"
            and right.category == "technology"
            and left.value == right.value
        ):
            return (
                self._id(left),
                "same_technology",
                self._id(right),
            )

        if (
            left.category == "architecture"
            and right.category == "architecture"
            and left.value == right.value
        ):
            return (
                self._id(left),
                "same_architecture",
                self._id(right),
            )

        return None

    def _id(
        self,
        observation: Observation,
    ) -> str:

        return (
            f"{observation.source}:"
            f"{observation.category}:"
            f"{observation.subject}:"
            f"{observation.value}"
        )

    def _observation_key(
        self,
        observation: Observation,
    ) -> tuple[str, str, str, str]:

        return (
            observation.source,
            observation.category,
            observation.subject,
            observation.value,
        )