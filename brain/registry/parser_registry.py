from pathlib import Path

from brain.exceptions.errors import UnsupportedFileTypeError
from brain.factories.parser_factory import ParserFactory
from brain.parser.base_parser import BaseParser


class ParserRegistry:
    """
    Stores and provides parsers based on file extension.
    """

    def __init__(self) -> None:
        self._parsers: dict[str, BaseParser] = {}

        for extension, parser in ParserFactory.create_parsers().items():
            self.register(extension, parser)

    def register(
        self,
        extension: str,
        parser: BaseParser,
    ) -> None:
        """
        Register a parser.
        """
        self._parsers[extension.lower()] = parser

    def get_parser(
        self,
        file_path: Path | str,
    ) -> BaseParser:
        """
        Retrieve the parser for a file.
        """
        extension = Path(file_path).suffix.lower()

        parser = self._parsers.get(extension)

        if parser is None:
            raise UnsupportedFileTypeError(extension)

        return parser