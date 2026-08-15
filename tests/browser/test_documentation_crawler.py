from brain.browser.crawlers.documentation_crawler import (
    DocumentationCrawler,
)


def test_documentation_crawler():

    html = """
    <a href="/docs">Docs</a>

    <a href="/installation">
        Installation
    </a>

    <a href="/configuration">
        Configuration
    </a>
    """

    links = (
        DocumentationCrawler()
    ).discover(
        html,
    )

    assert len(
        links,
    ) == 3

    assert (
        "/docs"
        in links
    )

    assert (
        "/installation"
        in links
    )

    assert (
        "/configuration"
        in links
    )