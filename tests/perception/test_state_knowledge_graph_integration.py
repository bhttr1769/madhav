from brain.perception.cross_modal_context_analyzer import (
    CrossModalContextAnalyzer,
)
from brain.perception.models.observation import (
    Observation,
)
from brain.perception.perception_graph_builder import (
    PerceptionGraphBuilder,
)
from brain.perception.perception_aggregator import (
    PerceptionAggregator,
)


def test_cross_modal_state_becomes_graph_knowledge():
    environment = Observation(
        source="environment",
        category="technology",
        subject="workspace",
        value="Python",
    )

    code = Observation(
        source="code",
        category="technology",
        subject="module",
        value="Python",
    )

    observations = PerceptionAggregator().aggregate(
        [
            environment,
            code,
        ]
    )

    context = CrossModalContextAnalyzer().analyze(
        observations,
    )

    graph = PerceptionGraphBuilder().build(
        context,
    )

    environment_id = (
        "environment:technology:"
        "workspace:Python"
    )

    code_id = (
        "code:technology:"
        "module:Python"
    )

    relationship_id = (
        f"{code_id}-same_technology-{environment_id}"
    )

    assert graph.graph.nodes[environment_id].name == "Python"
    assert graph.graph.nodes[code_id].name == "Python"

    edge = graph.graph.edges[relationship_id]

    assert edge.source == code_id
    assert edge.target == environment_id
    assert edge.relation == "same_technology"


def test_graph_contains_all_cross_modal_state_observations():
    observations = PerceptionAggregator().aggregate(
        [
            Observation(
                source="environment",
                category="architecture",
                subject="workspace",
                value="layered",
            ),
            Observation(
                source="code",
                category="architecture",
                subject="module",
                value="layered",
            ),
        ]
    )

    context = CrossModalContextAnalyzer().analyze(
        observations,
    )

    graph = PerceptionGraphBuilder().build(
        context,
    )

    assert (
        "environment:architecture:"
        "workspace:layered"
    ) in graph.graph.nodes

    assert (
        "code:architecture:"
        "module:layered"
    ) in graph.graph.nodes