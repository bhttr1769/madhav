from brain.graph.models.edge import Edge
from brain.graph.models.node import Node
from brain.graph.storage.graph_store import GraphStore


def test_graph_store():

    store = GraphStore()

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

    store.add_node(node)

    store.add_edge(edge)

    assert store.get_node("java") == node

    assert store.get_edge("1") == edge

    assert len(store.graph.nodes) == 1

    assert len(store.graph.edges) == 1
    
    
def test_neighbors():

    store = GraphStore()

    store.add_node(
        Node(
            id="java",
            name="Java",
            type="language",
        )
    )

    store.add_node(
        Node(
            id="spring",
            name="Spring Boot",
            type="framework",
        )
    )

    edge = Edge(
        id="1",
        source="java",
        target="spring",
        relation="USES",
    )

    store.add_edge(edge)

    neighbors = store.neighbors("java")

    assert len(neighbors) == 1

    assert neighbors[0] == edge