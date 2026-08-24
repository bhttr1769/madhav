from brain.knowledge.models.edge import (
    Edge,
)

from brain.knowledge.models.edge_type import (
    EdgeType,
)

from brain.knowledge.models.node import (
    Node,
)

from brain.knowledge.models.node_type import (
    NodeType,
)

from brain.knowledge.stores.graph_store import (
    GraphStore,
)


def create_node(
    node_id="node-1",
):

    return Node(
        id=node_id,
        type=NodeType.FILE,
        name="main.py",
        properties={},
        metadata={},
    )


def create_edge(
    edge_id="edge-1",
):

    return Edge(
        id=edge_id,
        source_id="node-1",
        target_id="node-2",
        type=EdgeType.IMPORTS,
        properties={},
        metadata={},
    )


def test_store_starts_empty():

    store = GraphStore()

    assert (
        store.node_count()
        == 0
    )

    assert (
        store.edge_count()
        == 0
    )

    assert (
        store.nodes()
        == []
    )

    assert (
        store.edges()
        == []
    )


def test_add_and_get_node():

    store = GraphStore()

    node = create_node()

    store.add_node(
        node,
    )

    assert (
        store.get_node(
            "node-1",
        )
        == node
    )


def test_get_missing_node():

    store = GraphStore()

    assert (
        store.get_node(
            "missing",
        )
        is None
    )


def test_nodes_returns_all_nodes():

    store = GraphStore()

    first = create_node(
        "node-1",
    )

    second = create_node(
        "node-2",
    )

    store.add_node(
        first,
    )

    store.add_node(
        second,
    )

    assert (
        store.nodes()
        == [
            first,
            second,
        ]
    )


def test_node_count():

    store = GraphStore()

    store.add_node(
        create_node(
            "node-1",
        )
    )

    store.add_node(
        create_node(
            "node-2",
        )
    )

    assert (
        store.node_count()
        == 2
    )


def test_remove_node():

    store = GraphStore()

    node = create_node()

    store.add_node(
        node,
    )

    removed = store.remove_node(
        "node-1",
    )

    assert (
        removed
        == node
    )

    assert (
        store.get_node(
            "node-1",
        )
        is None
    )

    assert (
        store.node_count()
        == 0
    )


def test_remove_missing_node():

    store = GraphStore()

    assert (
        store.remove_node(
            "missing",
        )
        is None
    )


def test_add_and_get_edge():

    store = GraphStore()

    edge = create_edge()

    store.add_edge(
        edge,
    )

    assert (
        store.get_edge(
            "edge-1",
        )
        == edge
    )


def test_get_missing_edge():

    store = GraphStore()

    assert (
        store.get_edge(
            "missing",
        )
        is None
    )


def test_edges_returns_all_edges():

    store = GraphStore()

    first = create_edge(
        "edge-1",
    )

    second = create_edge(
        "edge-2",
    )

    store.add_edge(
        first,
    )

    store.add_edge(
        second,
    )

    assert (
        store.edges()
        == [
            first,
            second,
        ]
    )


def test_edge_count():

    store = GraphStore()

    store.add_edge(
        create_edge(
            "edge-1",
        )
    )

    store.add_edge(
        create_edge(
            "edge-2",
        )
    )

    assert (
        store.edge_count()
        == 2
    )


def test_remove_edge():

    store = GraphStore()

    edge = create_edge()

    store.add_edge(
        edge,
    )

    removed = store.remove_edge(
        "edge-1",
    )

    assert (
        removed
        == edge
    )

    assert (
        store.get_edge(
            "edge-1",
        )
        is None
    )

    assert (
        store.edge_count()
        == 0
    )


def test_remove_missing_edge():

    store = GraphStore()

    assert (
        store.remove_edge(
            "missing",
        )
        is None
    )


def test_clear():

    store = GraphStore()

    store.add_node(
        create_node(),
    )

    store.add_edge(
        create_edge(),
    )

    store.clear()

    assert (
        store.node_count()
        == 0
    )

    assert (
        store.edge_count()
        == 0
    )