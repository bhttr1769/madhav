from pathlib import Path

from brain.models.document import Document
from brain.registry.parser_registry import ParserRegistry
from brain.registry.reader_registry import ReaderRegistry
from brain.registry.chunker_registry import ChunkerRegistry


class BrainManager:
    """
    Central entry point for reading and parsing documents.
    """

    def __init__(self) -> None:
        self._reader_registry = ReaderRegistry()
        self._parser_registry = ParserRegistry()
        self._chunker_registry = ChunkerRegistry()

    def read(self, file_path: Path | str) -> Document:
        file_path = Path(file_path)

        reader = self._reader_registry.get_reader(file_path)

        document = reader.read(file_path)

        parser = self._parser_registry.get_parser(file_path)

        document = parser.parse(document)
 
        chunker = self._chunker_registry.get_chunker()

        document.chunks = chunker.chunk(document)

        return document