from brain.perception.models.cross_modal_context import (
    CrossModalContext,
)

from brain.perception.models.observation import (
    Observation,
)

from brain.perception.perception_graph_builder import (
    PerceptionGraphBuilder,
)


def test_graph_builder_creates_observation_nodes():

    observation = Observation(
        source="workspace",
        category="technology",
        subject="project",
        value="Python",
        confidence=0.95,
    )

    context = CrossModalContext(
        observations=frozenset({
            observation,
        }),
        relationships=frozenset(),
    )

    graph = (
        PerceptionGraphBuilder().build(
            context,
        )
    )

    node = graph.graph.nodes[
        "workspace:technology:project:Python"
    ]

    assert node.name == "Python"
    assert node.type == "technology"
    assert node.metadata["source"] == "workspace"
    assert node.metadata["confidence"] == 0.95


def test_graph_builder_creates_relationships():

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

    relationship = (
        "code:technology:module:Python",
        "same_technology",
        "workspace:technology:project:Python",
    )

    context = CrossModalContext(
        observations=frozenset({
            first,
            second,
        }),
        relationships=frozenset({
            relationship,
        }),
    )

    graph = (
        PerceptionGraphBuilder().build(
            context,
        )
    )

    edge_id = (
        "code:technology:module:Python-"
        "same_technology-"
        "workspace:technology:project:Python"
    )

    edge = graph.graph.edges[
        edge_id
    ]

    assert edge.source == (
        "code:technology:module:Python"
    )

    assert edge.target == (
        "workspace:technology:project:Python"
    )

    assert edge.relation == (
        "same_technology"
    )


def test_graph_builder_handles_empty_context():

    context = CrossModalContext(
        observations=frozenset(),
        relationships=frozenset(),
    )

    graph = (
        PerceptionGraphBuilder().build(
            context,
        )
    )

    assert len(
        graph.graph.nodes
    ) == 0

    assert len(
        graph.graph.edges
    ) == 0