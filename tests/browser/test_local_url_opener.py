from brain.browser.openers.local_url_opener import (
    LocalUrlOpener,
)


def test_local_url_opener():

    opener = LocalUrlOpener()

    assert (
        opener
        is not None
    )