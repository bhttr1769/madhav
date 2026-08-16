import pytest

from brain.browser.clients.http_client import (
    HttpClient,
)
from tests.browser.fake_url_opener import (
    FakeUrlOpener,
)


def test_http_client():

    response = (
        HttpClient(
            FakeUrlOpener(),
        )
    ).get(
        "https://example.com"
    )

    assert response.status_code == 200

    assert len(
        response.content
    ) > 0