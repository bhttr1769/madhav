import pytest

from brain.graph.exceptions import (
    DuplicateEdgeError,
    DuplicateNodeError,
)
from brain.graph.models.edge import Edge
from brain.graph.models.node import Node
from brain.graph.storage.graph_store import GraphStore


def test_duplicate_node():

    store = GraphStore()

    node = Node(
        id="java",
        name="Java",
        type="language",
    )

    store.add_node(node)

    with pytest.raises(DuplicateNodeError):
        store.add_node(node)


def test_duplicate_edge():

    store = GraphStore()

    edge = Edge(
        id="1",
        source="java",
        target="spring",
        relation="USES",
    )

    store.add_edge(edge)

    with pytest.raises(DuplicateEdgeError):
        store.add_edge(edge)