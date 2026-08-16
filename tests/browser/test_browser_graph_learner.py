import pytest
from tests.browser.fake_graph_store import (
    FakeGraphStore,
)

from brain.browser.browser_engine import (
    BrowserEngine,
)

from brain.browser.browser_graph_learner import (
    BrowserGraphLearner,
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

def test_browser_graph_learner():

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

    engine = BrowserEngine(
        HttpClient(
            FakeUrlOpener(),
        ),
        loader_registry,
        parser_registry,
        extractor_registry,
        cleaner_registry,
    )

    graph = (
        FakeGraphStore()
    )

    learner = (
        BrowserGraphLearner(
            engine,
            graph,
        )
    )

    node = learner.learn(
        "https://example.com",
    )

    assert (
        node.id
        == "https://example.com"
    )

    assert (
        len(
            graph.nodes,
        )
        == 1
    )