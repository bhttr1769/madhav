from abc import ABC, abstractmethod

from brain.graph.models.edge import Edge
from brain.graph.models.node import Node


class RelationshipExtractor(ABC):
    """
    Extracts relationships between entities.
    """

    @abstractmethod
    def extract(
        self,
        text: str,
        nodes: list[Node],
    ) -> list[Edge]:
        """
        Extract relationships from text.
        """
        raise NotImplementedError