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


class QueryService:
    """
    Provides read and relationship queries
    over the knowledge graph.
    """

    def __init__(
        self,
        store: GraphStore,
    ):

        self._store = store

    def get_node(
        self,
        node_id: str,
    ) -> Node | None:

        return self._store.get_node(
            node_id,
        )

    def find_by_type(
        self,
        node_type: NodeType,
    ) -> list[Node]:

        return [
            node
            for node in self._store.nodes()
            if node.type == node_type
        ]

    def find_by_name(
        self,
        name: str,
    ) -> list[Node]:

        return [
            node
            for node in self._store.nodes()
            if node.name == name
        ]

    def find_by_name_contains(
        self,
        text: str,
    ) -> list[Node]:

        normalized = text.lower()

        return [
            node
            for node in self._store.nodes()
            if normalized
            in node.name.lower()
        ]

    def get_edge(
        self,
        edge_id: str,
    ) -> Edge | None:

        return self._store.get_edge(
            edge_id,
        )

    def outgoing_edges(
        self,
        node_id: str,
    ) -> list[Edge]:

        return [
            edge
            for edge in self._store.edges()
            if edge.source_id == node_id
        ]

    def incoming_edges(
        self,
        node_id: str,
    ) -> list[Edge]:

        return [
            edge
            for edge in self._store.edges()
            if edge.target_id == node_id
        ]

    def outgoing_edges_by_type(
        self,
        node_id: str,
        edge_type: EdgeType,
    ) -> list[Edge]:

        return [
            edge
            for edge in self.outgoing_edges(
                node_id,
            )
            if edge.type == edge_type
        ]

    def incoming_edges_by_type(
        self,
        node_id: str,
        edge_type: EdgeType,
    ) -> list[Edge]:

        return [
            edge
            for edge in self.incoming_edges(
                node_id,
            )
            if edge.type == edge_type
        ]

    def related_nodes(
        self,
        node_id: str,
    ) -> list[Node]:

        related = []

        for edge in self.outgoing_edges(
            node_id,
        ):

            node = self._store.get_node(
                edge.target_id,
            )

            if node is not None:

                related.append(
                    node,
                )

        return related

    def related_nodes_by_type(
        self,
        node_id: str,
        edge_type: EdgeType,
    ) -> list[Node]:

        related = []

        for edge in self.outgoing_edges_by_type(
            node_id,
            edge_type,
        ):

            node = self._store.get_node(
                edge.target_id,
            )

            if node is not None:

                related.append(
                    node,
                )

        return related