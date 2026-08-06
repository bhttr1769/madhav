from brain.graph.models.edge import Edge
from brain.graph.models.knowledge_graph import KnowledgeGraph
from brain.graph.models.node import Node


def test_knowledge_graph():

    graph = KnowledgeGraph()

    node = Node(
        id="java",
        name="Java",
        type="language",
    )

    edge = Edge(
        id="1",
        source="java",
        target="spring",
        relation="USES",
    )

    graph.nodes[node.id] = node

    graph.edges[edge.id] = edge

    assert len(graph.nodes) == 1

    assert len(graph.edges) == 1

    assert graph.nodes["java"].name == "Java"

    assert graph.edges["1"].relation == "USES"