from pathlib import Path

from brain.graph.models.edge import Edge
from brain.graph.models.node import Node
from brain.graph.persistence.graph_manager import (
    GraphManager,
)
from brain.graph.storage.graph_store import GraphStore


def test_graph_manager_save_and_load(
    tmp_path,
):

    path = tmp_path / "graph.json"

    store = GraphStore()

    store.add_node(
        Node(
            id="1",
            name="Java",
            type="language",
        )
    )

    store.add_node(
        Node(
            id="2",
            name="Spring Boot",
            type="framework",
        )
    )

    store.add_edge(
        Edge(
            id="1",
            source="1",
            target="2",
            relation="uses",
        )
    )

    manager = GraphManager(path)

    manager.save(store)

    loaded_store = manager.load()

    assert len(loaded_store.graph.nodes) == 2

    assert len(loaded_store.graph.edges) == 1