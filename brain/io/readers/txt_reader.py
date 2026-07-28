from pathlib import Path
from datetime import datetime

from brain.io.base_reader import BaseReader
from brain.models.document import Document


class TXTReader(BaseReader):
    """
    Reads a .txt file and converts it into a Document.
    """

    def read(self, file_path: Path) -> Document:
        file_path = Path(file_path)

        content = file_path.read_text(encoding="utf-8")

        stat = file_path.stat()

        return Document(
            name=file_path.name,
            path=file_path,
            extension=file_path.suffix,
            content=content,
            size=stat.st_size,
            created_at=datetime.fromtimestamp(stat.st_ctime),
            modified_at=datetime.fromtimestamp(stat.st_mtime),
        )