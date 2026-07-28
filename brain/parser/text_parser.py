from brain.models.document import Document
from brain.parser.base_parser import BaseParser


class TextParser(BaseParser):
    """
    Extracts basic statistics from a Document.
    """

    def parse(self, document: Document) -> Document:

        content = document.content

        lines = content.splitlines()
        words = content.split()
        characters = len(content)

        document.metadata["line_count"] = len(lines)
        document.metadata["word_count"] = len(words)
        document.metadata["character_count"] = characters
        document.metadata["empty_line_count"] = sum(
            1 for line in lines if not line.strip()
        )

        # Average reading speed ≈ 200 words/minute
        document.metadata["reading_time_minutes"] = max(
            1,
            round(len(words) / 200)
        )

        return document