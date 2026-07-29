from pathlib import Path

from docx import Document as DocxDocument

from brain.factories.document_factory import DocumentFactory
from brain.io.base_reader import BaseReader
from brain.models.document import Document


class DocxReader(BaseReader):
    """
    Reads DOCX files and converts them into Document objects.
    """

    def read(self, file_path: Path | str) -> Document:
        file_path = Path(file_path)

        doc = DocxDocument(file_path)

        text = "\n".join(
            paragraph.text
            for paragraph in doc.paragraphs
            if paragraph.text.strip()
        )

        return DocumentFactory.create(
            file_path=file_path,
            content=text,
        )