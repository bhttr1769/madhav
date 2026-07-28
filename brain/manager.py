from pathlib import Path

from brain.exceptions.errors import UnsupportedFileTypeError
from brain.models.document import Document
from brain.registry.parser_registry import ParserRegistry
from brain.registry.reader_registry import ReaderRegistry


class BrainManager:
    """
    Central entry point for reading and parsing documents.
    """

    def __init__(self) -> None:
        self._reader_registry = ReaderRegistry()
        self._parser_registry = ParserRegistry()

    def read(self, file_path: Path | str) -> Document:
        file_path = Path(file_path)

        reader = self._reader_registry.get_reader(file_path)

        if reader is None:
            raise UnsupportedFileTypeError(
                f"Unsupported file type: {file_path.suffix}"
            )

        document = reader.read(file_path)

        parser = self._parser_registry.get_parser(file_path)

        if parser is not None:
            document = parser.parse(document)

        return document