from brain.graph.models.edge import Edge
from brain.graph.models.knowledge_graph import KnowledgeGraph
from brain.graph.models.node import Node

from brain.graph.exceptions import (
    DuplicateEdgeError,
    DuplicateNodeError,
)


class GraphStore:
    """
    Stores and manages the knowledge graph.
    """

    def __init__(self):

        self._graph = KnowledgeGraph()

    @property
    def graph(self) -> KnowledgeGraph:

        return self._graph

    def add_node(
        self,
        node: Node,
    ) -> None:

        if node.id in self._graph.nodes:
            raise DuplicateNodeError(
                f"Node '{node.id}' already exists."
            )

        self._graph.nodes[node.id] = node

    def add_edge(
        self,
        edge: Edge,
    ) -> None:

        if edge.id in self._graph.edges:
            raise DuplicateEdgeError(
                f"Edge '{edge.id}' already exists."
            )

        self._graph.edges[edge.id] = edge

    def get_node(
        self,
        node_id: str,
    ) -> Node | None:

        return self._graph.nodes.get(node_id)

    def get_edge(
        self,
        edge_id: str,
    ) -> Edge | None:

        return self._graph.edges.get(edge_id)

    def neighbors(
        self,
        node_id: str,
    ) -> list[Edge]:
        """
        Return all outgoing relationships
        for a node.
        """

        return [
            edge
            for edge in self._graph.edges.values()
            if edge.source == node_id
        ]