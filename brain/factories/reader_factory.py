from brain.io.readers.docx_reader import DocxReader
from brain.io.readers.pdf_reader import PDFReader
from brain.io.readers.txt_reader import TXTReader


class ReaderFactory:
    """
    Factory responsible for creating reader instances.
    """

    @staticmethod
    def create_readers() -> dict:
        return {
            ".txt": TXTReader(),
            ".pdf": PDFReader(),
            ".docx": DocxReader(),
        }