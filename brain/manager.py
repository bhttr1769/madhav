from pathlib import Path

from brain.models.document import Document
from brain.config.brain_config import BrainConfig


class BrainManager:
    """
    Central entry point for reading and parsing documents.
    """

    def __init__(self, config: BrainConfig) -> None:
        self._config = config

    def read(self, file_path: Path | str) -> Document:
        file_path = Path(file_path)

        reader = self._config.reader_registry.get_reader(file_path)

        document = reader.read(file_path)

        parser = self._config.parser_registry.get_parser(file_path)

        document = parser.parse(document)

        chunker = self._config.chunker_registry.get_chunker()

        document.chunks = chunker.chunk(document)

        return document