from uuid import uuid4
from typing import Any

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


class GraphBuilder:
    """
    Builds knowledge graph nodes and relationships
    using a GraphStore.
    """

    def __init__(
        self,
        store: GraphStore,
    ):

        self._store = store

    def add_node(
        self,
        node_type: NodeType,
        name: str,
        properties: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
        node_id: str | None = None,
    ) -> Node:

        node = Node(
            id=(
                node_id
                if node_id is not None
                else str(uuid4())
            ),
            type=node_type,
            name=name,
            properties=(
                dict(properties)
                if properties is not None
                else {}
            ),
            metadata=(
                dict(metadata)
                if metadata is not None
                else {}
            ),
        )

        self._store.add_node(
            node,
        )

        return node

    def add_edge(
        self,
        source_id: str,
        target_id: str,
        edge_type: EdgeType,
        properties: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
        edge_id: str | None = None,
    ) -> Edge:

        if (
            self._store.get_node(
                source_id,
            )
            is None
        ):

            raise ValueError(
                f"Source node does not exist: "
                f"{source_id}"
            )

        if (
            self._store.get_node(
                target_id,
            )
            is None
        ):

            raise ValueError(
                f"Target node does not exist: "
                f"{target_id}"
            )

        edge = Edge(
            id=(
                edge_id
                if edge_id is not None
                else str(uuid4())
            ),
            source_id=source_id,
            target_id=target_id,
            type=edge_type,
            properties=(
                dict(properties)
                if properties is not None
                else {}
            ),
            metadata=(
                dict(metadata)
                if metadata is not None
                else {}
            ),
        )

        self._store.add_edge(
            edge,
        )

        return edge