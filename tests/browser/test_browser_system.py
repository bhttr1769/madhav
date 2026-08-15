from tests.browser.fake_graph_store import (
    FakeGraphStore,
)

from tests.browser.fake_memory import (
    FakeMemory,
)

from brain.browser.browser_engine import (
    BrowserEngine,
)

from brain.browser.browser_graph_learner import (
    BrowserGraphLearner,
)

from brain.browser.browser_memory_learner import (
    BrowserMemoryLearner,
)

from brain.browser.browser_system import (
    BrowserSystem,
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


def test_browser_system():

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
        HttpClient(),
        loader_registry,
        parser_registry,
        extractor_registry,
        cleaner_registry,
    )

    memory = FakeMemory()

    graph = (
        FakeGraphStore()
    )

    memory_learner = (
        BrowserMemoryLearner(
            engine,
            memory,
        )
    )

    graph_learner = (
        BrowserGraphLearner(
            engine,
            graph,
        )
    )

    system = BrowserSystem(
        memory_learner,
        graph_learner,
    )

    system.learn(
        "https://example.com",
    )

    assert (
        len(
            memory.items,
        )
        == 1
    )

    assert (
        len(
            graph.nodes,
        )
        == 1
    )