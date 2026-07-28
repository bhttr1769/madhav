from datetime import datetime
from pathlib import Path

from brain.models.document import Document
from brain.parser.text_parser import TextParser


def test_text_parser():

    document = Document(
        name="sample.txt",
        path=Path("sample.txt"),
        extension=".txt",
        content="Hello Madhav!\n\nThis is my first document.",
        size=42,
        created_at=datetime.now(),
        modified_at=datetime.now(),
    )

    parser = TextParser()

    parsed = parser.parse(document)

    assert parsed.metadata["line_count"] == 3
    assert parsed.metadata["word_count"] == 7
    assert parsed.metadata["character_count"] > 0
    assert parsed.metadata["empty_line_count"] == 1
    assert parsed.metadata["reading_time_minutes"] == 1