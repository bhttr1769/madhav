from brain.graph.models.edge import Edge


def test_edge():

    edge = Edge(
        id="1",
        source="java",
        target="spring_boot",
        relation="USES",
    )

    assert edge.id == "1"

    assert edge.source == "java"

    assert edge.target == "spring_boot"

    assert edge.relation == "USES"

    assert edge.metadata == {}