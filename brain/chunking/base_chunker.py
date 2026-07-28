from abc import ABC, abstractmethod

from brain.models.chunk import Chunk
from brain.models.document import Document


class BaseChunker(ABC):
    """
    Base class for all chunking strategies.
    """

    @abstractmethod
    def chunk(self, document: Document) -> list[Chunk]:
        """
        Split a document into chunks.
        """
        pass