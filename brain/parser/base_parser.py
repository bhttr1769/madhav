from abc import ABC, abstractmethod

from brain.models.document import Document


class BaseParser(ABC):
    """
    Base class for all parsers.
    """

    @abstractmethod
    def parse(self, document: Document) -> Document:
        """
        Parse a Document and return the enriched Document.
        """
        raise NotImplementedError