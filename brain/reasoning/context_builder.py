from brain.perception.models.cross_modal_context import (
    CrossModalContext,
)

from brain.reasoning.models.context import (
    Context,
)


class ContextBuilder:
    """
    Builds reasoning context from perception results.
    """

    def build(
        self,
        perception: CrossModalContext,
        facts: frozenset[str] = frozenset(),
        constraints: frozenset[str] = frozenset(),
        goals: frozenset[str] = frozenset(),
    ) -> Context:

        observations = frozenset(
            self._observation_text(
                observation,
            )
            for observation
            in perception.observations
        )

        return Context(
            observations=observations,
            facts=facts,
            constraints=constraints,
            goals=goals,
        )

    def _observation_text(
        self,
        observation,
    ) -> str:

        return (
            f"{observation.source}:"
            f"{observation.category}:"
            f"{observation.subject}:"
            f"{observation.value}"
        )