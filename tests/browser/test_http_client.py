from brain.browser.clients.http_client import (
    HttpClient,
)


def test_http_client():

    response = (
        HttpClient()
    ).get(
        "https://example.com"
    )

    assert (
        response.status_code
        == 200
    )

    assert (
        len(
            response.content
        )
        > 0
    )