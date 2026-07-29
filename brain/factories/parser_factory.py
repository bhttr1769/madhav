from brain.config.parsing_config import ParsingConfig
from brain.parser.text_parser import TextParser


class ParserFactory:
    """
    Factory responsible for creating parser instances.
    """

    @staticmethod
    def create_parsers() -> dict:
        return {
        ".txt": TextParser(
            config=ParsingConfig()
        ),
        ".pdf": TextParser(
            config=ParsingConfig()
        ),
        ".docx": TextParser(
            config=ParsingConfig()
        )
    }