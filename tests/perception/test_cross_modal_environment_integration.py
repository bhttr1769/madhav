from brain.perception.cross_modal_context_analyzer import (
    CrossModalContextAnalyzer,
)
from brain.perception.models.observation import (
    Observation,
)
from brain.perception.perception_aggregator import (
    PerceptionAggregator,
)


def test_environment_observations_participate_in_cross_modal_understanding():
    environment_observation = Observation(
        source="environment",
        category="technology",
        subject="workspace",
        value="Python",
    )

    code_observation = Observation(
        source="code",
        category="technology",
        subject="module",
        value="Python",
    )

    aggregated = PerceptionAggregator().aggregate(
        [
            environment_observation,
            code_observation,
        ]
    )

    context = CrossModalContextAnalyzer().analyze(
        aggregated,
    )

    assert (
        (
            "code:technology:module:Python",
            "same_technology",
            "environment:technology:workspace:Python",
        )
        in context.relationships
    )


def test_cross_modal_context_preserves_aggregated_observations():
    observations = frozenset(
        {
            Observation(
                source="environment",
                category="technology",
                subject="workspace",
                value="Python",
            ),
            Observation(
                source="code",
                category="technology",
                subject="module",
                value="Python",
            ),
        }
    )

    aggregated = PerceptionAggregator().aggregate(
        list(observations)
    )

    context = CrossModalContextAnalyzer().analyze(
        aggregated,
    )

    assert context.observations == aggregated