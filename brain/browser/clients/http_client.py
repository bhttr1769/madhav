import urllib.request

from brain.browser.models.response import (
    Response,
)


class HttpClient:
    """
    Retrieves content from URLs.
    """

    def get(
        self,
        url: str,
    ) -> Response:

        with urllib.request.urlopen(
            url,
            timeout=10,
        ) as response:

            content = (
                response.read()
                .decode(
                    "utf-8",
                )
            )

            return Response(
                url=url,
                status_code=response.status,
                content=content,
            )