from pathlib import Path

from brain.io.base_reader import BaseReader
from brain.io.readers.txt_reader import TXTReader


class ReaderRegistry:
    """
    Stores and provides file readers based on file extension.
    """

    def __init__(self) -> None:
        self._readers: dict[str, BaseReader] = {}

        self.register(".txt", TXTReader())

    def register(self, extension: str, reader: BaseReader) -> None:
        """
        Register a reader for a file extension.
        """
        self._readers[extension.lower()] = reader

    def get_reader(self, file_path: Path | str) -> BaseReader | None:
        """
        Return the reader for the given file.
        """
        extension = Path(file_path).suffix.lower()

        return self._readers.get(extension)