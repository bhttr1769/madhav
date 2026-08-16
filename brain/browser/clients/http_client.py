from brain.browser.models.response import (
    Response,
)


class HttpClient:

    def __init__(
        self,
        opener,
    ):

        self._opener = opener

    def get(
        self,
        url: str,
    ) -> Response:

        with self._opener.open(
            url,
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