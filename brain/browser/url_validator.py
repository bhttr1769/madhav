from urllib.parse import urlparse


class UrlValidator:
    """
    Validates and normalizes URLs.
    """

    def normalize(
        self,
        url: str,
    ) -> str:

        url = url.strip()

        if not url.startswith(
            (
                "http://",
                "https://",
            )
        ):

            url = (
                f"https://{url}"
            )

        return url

    def is_valid(
        self,
        url: str,
    ) -> bool:

        url = self.normalize(
            url,
        )

        parsed = urlparse(
            url,
        )

        return bool(
            parsed.scheme
            and parsed.netloc
        )