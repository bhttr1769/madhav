from brain.browser.models.document import (
    Document,
)

from brain.browser.parsers.html_parser import (
    HtmlParser,
)


def test_html_parser():

    html = """
    <html>
        <head>
            <title>Madhav</title>
        </head>
    </html>
    """

    document = (
        HtmlParser()
    ).parse(
        html,
    )

    assert isinstance(
        document,
        Document,
    )

    assert (
        document.title
        == "Madhav"
    )