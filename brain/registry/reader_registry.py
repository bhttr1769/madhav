from pathlib import Path

from brain.exceptions.errors import UnsupportedFileTypeError
from brain.io.base_reader import BaseReader
from brain.io.readers.txt_reader import TXTReader
from brain.io.readers.pdf_reader import PDFReader
from brain.io.readers.docx_reader import DocxReader


class ReaderRegistry:
    """
    Stores and provides file readers based on file extension.
    """

    def __init__(self) -> None:
        self._readers: dict[str, BaseReader] = {}

        self.register(".txt", TXTReader())
        self.register(".pdf", PDFReader())
        self.register(".docx", DocxReader())

    def register(self, extension: str, reader: BaseReader) -> None:
        """
        Register a reader for a file extension.
        """
        self._readers[extension.lower()] = reader

    def get_reader(self, file_path: Path | str) -> BaseReader:
        """
        Return the reader for the given file.
        """
        extension = Path(file_path).suffix.lower()

        reader = self._readers.get(extension)

        if reader is None:
            raise UnsupportedFileTypeError(extension)

        return reader