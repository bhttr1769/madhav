import math
from brain.models.document import Document
from brain.parser.base_parser import BaseParser
from brain.config.parsing_config import ParsingConfig


class TextParser(BaseParser):
    """
    Extracts basic statistics from a Document.
    """

    def __init__(self, config: ParsingConfig):
        self._config = config

    def parse(self, document: Document) -> Document:

        content = document.content

        lines = content.splitlines()
        words = content.split()

        word_count = len(words)
        character_count = len(content)

        document.metadata["line_count"] = len(lines)
        document.metadata["word_count"] = word_count
        document.metadata["character_count"] = character_count
        document.metadata["empty_line_count"] = sum(
            1 for line in lines if not line.strip()
        )

        reading_time = math.ceil(
            word_count / self._config.reading_speed_wpm
        )     

        document.metadata["reading_time_minutes"] = reading_time

        return document