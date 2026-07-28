from pathlib import Path

from brain.io.readers.txt_reader import TXTReader
from brain.models.document import Document
from brain.parser.text_parser import TextParser


class BrainManager:
    """
    Central entry point for reading and parsing documents.
    """

    def __init__(self) -> None:
        self._readers = {
            ".txt": TXTReader(),
        }

        self._parsers = {
            ".txt": TextParser(),
        }

    def read(self, file_path: Path | str) -> Document:
        """
        Read a supported file and return an enriched Document.
        """

        file_path = Path(file_path)
        extension = file_path.suffix.lower()

        reader = self._readers.get(extension)

        if reader is None:
            raise ValueError(f"Unsupported file type: {extension}")

        document = reader.read(file_path)

        parser = self._parsers.get(extension)

        if parser is not None:
            document = parser.parse(document)

        return document