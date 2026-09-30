from brain.perception.cross_modal_context_analyzer import (
    CrossModalContextAnalyzer,
)

from brain.perception.models.cross_modal_context import (
    CrossModalContext,
)

from brain.perception.models.observation import (
    Observation,
)

from brain.perception.perception_graph_builder import (
    PerceptionGraphBuilder,
)


def test_observation_accepts_valid_confidence_values():

    for confidence in (
        0.0,
        0.25,
        0.5,
        0.95,
        1.0,
    ):
        observation = Observation(
            source="workspace",
            category="technology",
            subject="project",
            value="Python",
            confidence=confidence,
        )

        assert observation.confidence == confidence


def test_observation_preserves_required_fields():

    observation = Observation(
        source="workspace",
        category="technology",
        subject="project",
        value="Python",
    )

    assert observation.source
    assert observation.category
    assert observation.subject
    assert observation.value


def test_cross_modal_context_preserves_observations():

    observation = Observation(
        source="workspace",
        category="technology",
        subject="project",
        value="Python",
    )

    context = CrossModalContext(
        observations=frozenset({
            observation,
        }),
        relationships=frozenset(),
    )

    assert context.observations == frozenset({
        observation,
    })


def test_cross_modal_relationship_references_existing_observations():

    first = Observation(
        source="workspace",
        category="technology",
        subject="project",
        value="Python",
    )

    second = Observation(
        source="code",
        category="technology",
        subject="module",
        value="Python",
    )

    context = CrossModalContextAnalyzer().analyze(
        frozenset({
            first,
            second,
        })
    )

    observation_ids = {
        (
            f"{observation.source}:"
            f"{observation.category}:"
            f"{observation.subject}:"
            f"{observation.value}"
        )
        for observation in context.observations
    }

    for source_id, _, target_id in context.relationships:
        assert source_id in observation_ids
        assert target_id in observation_ids


def test_cross_modal_context_does_not_create_unsupported_relationships():

    first = Observation(
        source="workspace",
        category="technology",
        subject="project",
        value="Python",
    )

    second = Observation(
        source="ui",
        category="element",
        subject="button",
        value="Submit",
    )

    context = CrossModalContextAnalyzer().analyze(
        frozenset({
            first,
            second,
        })
    )

    assert context.relationships == frozenset()


def test_perception_graph_preserves_observation_confidence():

    observation = Observation(
        source="workspace",
        category="technology",
        subject="project",
        value="Python",
        confidence=0.75,
    )

    context = CrossModalContext(
        observations=frozenset({
            observation,
        }),
        relationships=frozenset(),
    )

    graph = PerceptionGraphBuilder().build(
        context,
    )

    node = graph.graph.nodes[
        "workspace:technology:project:Python"
    ]

    assert node.metadata["confidence"] == 0.75


def test_perception_pipeline_is_deterministic():

    observations = frozenset({
        Observation(
            source="workspace",
            category="technology",
            subject="project",
            value="Python",
        ),
        Observation(
            source="code",
            category="technology",
            subject="module",
            value="Python",
        ),
        Observation(
            source="workspace",
            category="architecture",
            subject="project",
            value="layered",
        ),
        Observation(
            source="code",
            category="architecture",
            subject="module",
            value="layered",
        ),
    })

    analyzer = CrossModalContextAnalyzer()

    first = analyzer.analyze(
        observations,
    )

    second = analyzer.analyze(
        observations,
    )

    assert first == second

    first_graph = PerceptionGraphBuilder().build(
        first,
    )

    second_graph = PerceptionGraphBuilder().build(
        second,
    )

    assert (
        first_graph.graph.nodes
        == second_graph.graph.nodes
    )

    assert (
        first_graph.graph.edges
        == second_graph.graph.edges
    )