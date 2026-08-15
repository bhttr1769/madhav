from brain.browser.loaders.html_loader import (
    HtmlLoader,
)

from brain.browser.models.response import (
    Response,
)


def test_html_loader():

    response = Response(
        url="https://example.com",
        status_code=200,
        content=(
            "<html>"
            "<body>Hello</body>"
            "</html>"
        ),
    )

    loader = (
        HtmlLoader()
    )

    assert loader.can_load(
        response,
    )

    assert (
        loader.load(
            response,
        )
        == response.content
    )