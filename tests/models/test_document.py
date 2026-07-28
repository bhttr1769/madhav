from pathlib import Path
from datetime import datetime

from brain.models.document import Document


def test_document_creation():

    doc = Document(
        name="notes.txt",
        path=Path("notes.txt"),
        extension=".txt",
        content="Hello Madhav",
        size=12,
        created_at=datetime.now(),
        modified_at=datetime.now(),
    )

    assert doc.name == "notes.txt"

    assert doc.extension == ".txt"

    assert doc.content == "Hello Madhav"