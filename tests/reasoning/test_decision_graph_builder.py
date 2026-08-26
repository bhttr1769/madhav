from brain.reasoning.decision_graph_builder import (
    DecisionGraphBuilder,
)

from brain.reasoning.models.decision import (
    Decision,
)


def test_builder_creates_decision_node():

    decision = Decision(
        action="inspect architecture",
        rationale="Architecture is incomplete.",
        confidence=0.9,
        alternatives=frozenset(),
    )

    graph = DecisionGraphBuilder().build(
        decision,
    )

    node = graph.graph.nodes[
        "decision"
    ]

    assert node.name == (
        "inspect architecture"
    )

    assert node.type == "decision"

    assert node.metadata["rationale"] == (
        "Architecture is incomplete."
    )

    assert node.metadata["confidence"] == 0.9


def test_builder_creates_alternatives():

    decision = Decision(
        action="inspect architecture",
        rationale="Architecture is incomplete.",
        confidence=0.9,
        alternatives=frozenset({
            "inspect dependencies",
            "inspect source",
        }),
    )

    graph = DecisionGraphBuilder().build(
        decision,
    )

    assert len(
        graph.graph.nodes
    ) == 3

    assert len(
        graph.graph.edges
    ) == 2

    alternatives = {
        graph.graph.nodes[
            f"alternative:{index}"
        ].name
        for index in range(2)
    }

    assert alternatives == {
        "inspect dependencies",
        "inspect source",
    }


def test_builder_handles_no_alternatives():

    decision = Decision(
        action="continue",
        rationale="No additional action required.",
        confidence=1.0,
        alternatives=frozenset(),
    )

    graph = DecisionGraphBuilder().build(
        decision,
    )

    assert len(
        graph.graph.nodes
    ) == 1

    assert len(
        graph.graph.edges
    ) == 0