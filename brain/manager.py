from pathlib import Path

from brain.io.readers.txt_reader import TXTReader
from brain.models.document import Document


class BrainManager:
    """
    Central entry point for reading documents into the Brain.
    """

    def __init__(self) -> None:
        self._readers = {
            ".txt": TXTReader(),
        }

    def read(self, file_path: Path | str) -> Document:
        """
        Read a supported file and return a Document.
        """

        file_path = Path(file_path)

        extension = file_path.suffix.lower()

        reader = self._readers.get(extension)

        if reader is None:
            raise ValueError(f"Unsupported file type: {extension}")

        return reader.read(file_path)