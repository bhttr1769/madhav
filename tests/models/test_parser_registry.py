from brain.parser.text_parser import TextParser
from brain.registry.parser_registry import ParserRegistry


def test_parser_registry_returns_text_parser():

    registry = ParserRegistry()

    parser = registry.get_parser("sample.txt")

    assert isinstance(parser, TextParser)