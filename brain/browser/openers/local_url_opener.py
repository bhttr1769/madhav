import urllib.request

from brain.browser.openers.base_url_opener import (
    BaseUrlOpener,
)


class LocalUrlOpener(
    BaseUrlOpener,
):

    def open(
        self,
        url: str,
    ):

        return urllib.request.urlopen(
            url,
            timeout=10,
        )