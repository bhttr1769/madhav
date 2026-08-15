from brain.browser.extractors.html_extractor import (
    HtmlExtractor,
)

from brain.browser.registries.extractor_registry import (
    ExtractorRegistry,
)


def test_extractor_registry():

    registry = (
        ExtractorRegistry()
    )

    registry.register(
        HtmlExtractor(),
    )

    assert (
        len(
            registry.all()
        )
        == 1
    )