from brain.knowledge.models.edge import (
    Edge,
)

from brain.knowledge.models.node import (
    Node,
)


class GraphStore:
    """
    Stores knowledge graph nodes and edges.
    """

    def __init__(
        self,
    ):

        self._nodes = {}

        self._edges = {}

    def add_node(
        self,
        node: Node,
    ) -> None:

        self._nodes[
            node.id
        ] = node

    def get_node(
        self,
        node_id: str,
    ) -> Node | None:

        return self._nodes.get(
            node_id,
        )

    def remove_node(
        self,
        node_id: str,
    ) -> Node | None:

        return self._nodes.pop(
            node_id,
            None,
        )

    def nodes(
        self,
    ) -> list[Node]:

        return list(
            self._nodes.values(),
        )

    def add_edge(
        self,
        edge: Edge,
    ) -> None:

        self._edges[
            edge.id
        ] = edge

    def get_edge(
        self,
        edge_id: str,
    ) -> Edge | None:

        return self._edges.get(
            edge_id,
        )

    def remove_edge(
        self,
        edge_id: str,
    ) -> Edge | None:

        return self._edges.pop(
            edge_id,
            None,
        )

    def edges(
        self,
    ) -> list[Edge]:

        return list(
            self._edges.values(),
        )

    def node_count(
        self,
    ) -> int:

        return len(
            self._nodes,
        )

    def edge_count(
        self,
    ) -> int:

        return len(
            self._edges,
        )

    def clear(
        self,
    ) -> None:

        self._nodes.clear()

        self._edges.clear()