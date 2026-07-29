from datetime import datetime
from pathlib import Path

from brain.models.document import Document


class DocumentFactory:
    """
    Creates Document objects from files.
    """

    @staticmethod
    def create(file_path: Path | str, content: str) -> Document:
        file_path = Path(file_path)

        stat = file_path.stat()

        return Document(
            name=file_path.name,
            path=file_path,
            extension=file_path.suffix.lower(),
            content=content,
            size=stat.st_size,
            created_at=datetime.fromtimestamp(stat.st_ctime),
            modified_at=datetime.fromtimestamp(stat.st_mtime),
        )