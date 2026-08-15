from brain.browser.extractors.html_extractor import (
    HtmlExtractor,
)

from brain.browser.models.document import (
    Document,
)


def test_html_extractor():

    document = Document(
        title="Test",
        content=(
            "<html>"
            "<body>"
            "<h1>Hello</h1>"
            "<p>World</p>"
            "</body>"
            "</html>"
        ),
    )

    extracted = (
        HtmlExtractor()
    ).extract(
        document,
    )

    assert (
        "Hello"
        in extracted.text
    )

    assert (
        "World"
        in extracted.text
    )