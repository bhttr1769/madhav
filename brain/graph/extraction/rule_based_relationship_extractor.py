from brain.graph.extraction.relationship_extractor import (
    RelationshipExtractor,
)
from brain.graph.models.edge import Edge
from brain.graph.models.node import Node


class RuleBasedRelationshipExtractor(
    RelationshipExtractor,
):
    """
    Simple rule-based relationship extractor.
    """

    def extract(
        self,
        text: str,
        nodes: list[Node],
    ) -> list[Edge]:

        edges = []

        if (
            "uses" in text.lower()
            and len(nodes) >= 2
        ):

            edge = Edge(
                id=f"{nodes[0].id}-uses-{nodes[1].id}",
                source=nodes[0].id,
                target=nodes[1].id,
                relation="USES",
            )

            edges.append(edge)

        return edges