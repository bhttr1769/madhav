from pathlib import Path

from brain.models.document import Document
from brain.parser.text_parser import TextParser
from brain.registry.reader_registry import ReaderRegistry


class BrainManager:
    """
    Central entry point for reading and parsing documents.
    """

    def __init__(self) -> None:
        self._reader_registry = ReaderRegistry()

        self._parsers = {
            ".txt": TextParser(),
        }

    def read(self, file_path: Path | str) -> Document:
        file_path = Path(file_path)

        reader = self._reader_registry.get_reader(file_path)

        if reader is None:
            raise ValueError(f"Unsupported file type: {file_path.suffix}")

        document = reader.read(file_path)

        parser = self._parsers.get(file_path.suffix.lower())

        if parser is not None:
            document = parser.parse(document)

        return document