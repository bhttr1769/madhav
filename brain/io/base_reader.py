from abc import ABC, abstractmethod
from pathlib import Path

from brain.models.document import Document


class BaseReader(ABC):
    """
    Base class for all file readers.
    """

    @abstractmethod
    def read(self, file_path: Path) -> Document:
        """
        Read a file and convert it into a Document.
        """
        raise NotImplementedError