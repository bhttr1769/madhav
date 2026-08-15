import re


class DocumentationCrawler:
    """
    Discovers links in documentation.
    """

    def discover(
        self,
        html: str,
    ) -> list[str]:

        return re.findall(
            r'href=["\'](.*?)["\']',
            html,
        )