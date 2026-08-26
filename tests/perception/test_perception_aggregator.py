from brain.perception.models.observation import (
    Observation,
)

from brain.perception.perception_aggregator import (
    PerceptionAggregator,
)


def test_aggregator_collects_observations():

    observations = [
        Observation(
            source="workspace",
            category="technology",
            subject="project",
            value="Python",
        ),
        Observation(
            source="ui",
            category="element",
            subject="button",
            value="Submit",
        ),
    ]

    result = (
        PerceptionAggregator().aggregate(
            observations,
        )
    )

    assert result == frozenset(
        observations
    )


def test_aggregator_handles_empty_input():

    result = (
        PerceptionAggregator().aggregate(
            [],
        )
    )

    assert result == frozenset()


def test_aggregator_deduplicates_observations():

    observation = Observation(
        source="workspace",
        category="technology",
        subject="project",
        value="Python",
    )

    result = (
        PerceptionAggregator().aggregate(
            [
                observation,
                observation,
            ],
        )
    )

    assert result == frozenset({
        observation,
    })