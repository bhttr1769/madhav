from abc import ABC, abstractmethod

from brain.graph.models.node import Node


class EntityExtractor(ABC):
    """
    Extracts knowledge entities from text.
    """

    @abstractmethod
    def extract(
        self,
        text: str,
    ) -> list[Node]:
        """
        Extract entities from text.
        """
        raise NotImplementedError