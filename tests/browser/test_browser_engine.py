import pytest
from brain.browser.browser_engine import (
    BrowserEngine,
)

from brain.browser.cleaners.text_cleaner import (
    TextCleaner,
)

from brain.browser.clients.http_client import (
    HttpClient,
)

from brain.browser.extractors.html_extractor import (
    HtmlExtractor,
)

from brain.browser.loaders.html_loader import (
    HtmlLoader,
)

from brain.browser.parsers.html_parser import (
    HtmlParser,
)

from brain.browser.registries.cleaner_registry import (
    CleanerRegistry,
)

from brain.browser.registries.extractor_registry import (
    ExtractorRegistry,
)

from brain.browser.registries.loader_registry import (
    LoaderRegistry,
)

from brain.browser.registries.parser_registry import (
    ParserRegistry,
)

from tests.browser.fake_url_opener import (
    FakeUrlOpener,
)


def test_browser_engine():

    loader_registry = (
        LoaderRegistry()
    )

    loader_registry.register(
        HtmlLoader(),
    )

    parser_registry = (
        ParserRegistry()
    )

    parser_registry.register(
        HtmlParser(),
    )

    extractor_registry = (
        ExtractorRegistry()
    )

    extractor_registry.register(
        HtmlExtractor(),
    )

    cleaner_registry = (
        CleanerRegistry()
    )

    cleaner_registry.register(
        TextCleaner(),
    )

    result = BrowserEngine(
        HttpClient(
            FakeUrlOpener(),
        ),
        loader_registry,
        parser_registry,
        extractor_registry,
        cleaner_registry,
    ).learn(
        "https://example.com",
    )

    assert len(
        result.text
    ) > 0