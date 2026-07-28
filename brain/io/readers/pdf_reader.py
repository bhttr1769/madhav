from pathlib import Path

from pypdf import PdfReader as PyPdfReader

from brain.factory.document_factory import DocumentFactory
from brain.io.base_reader import BaseReader
from brain.models.document import Document


class PDFReader(BaseReader):
    """
    Reads PDF files and converts them into Document objects.
    """

    def read(self, file_path: Path | str) -> Document:
        file_path = Path(file_path)
        stat = file_path.stat()

        reader = PyPdfReader(file_path)

        text = ""

        for page in reader.pages:
            extracted = page.extract_text()

            if extracted:
                text += extracted + "\n"

        return DocumentFactory.create(
            file_path=file_path,
            content=text,
        )