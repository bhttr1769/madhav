from brain.browser.parsers.html_parser import (
    HtmlParser,
)

from brain.browser.registries.parser_registry import (
    ParserRegistry,
)


def test_parser_registry():

    registry = (
        ParserRegistry()
    )

    registry.register(
        HtmlParser(),
    )

    assert (
        len(
            registry.all()
        )
        == 1
    )