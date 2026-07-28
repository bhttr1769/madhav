from pathlib import Path

from brain.parser.base_parser import BaseParser
from brain.parser.text_parser import TextParser


class ParserRegistry:
    """
    Stores and provides parsers based on file extension.
    """

    def __init__(self) -> None:
        self._parsers: dict[str, BaseParser] = {}

        self.register(".txt", TextParser())

    def register(self, extension: str, parser: BaseParser) -> None:
        """
        Register a parser for a file extension.
        """
        self._parsers[extension.lower()] = parser

    def get_parser(self, file_path: Path | str) -> BaseParser | None:
        """
        Return the parser for the given file.
        """
        extension = Path(file_path).suffix.lower()
        return self._parsers.get(extension)