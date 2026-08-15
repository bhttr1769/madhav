import re

from brain.browser.models.document import (
    Document,
)

from brain.browser.parsers.base_parser import (
    BaseParser,
)


class HtmlParser(
    BaseParser,
):

    def can_parse(
        self,
        content: str,
    ) -> bool:

        return (
            "<html"
            in content.lower()
        )

    def parse(
        self,
        content: str,
    ) -> Document:

        title = ""

        match = re.search(
            r"<title>(.*?)</title>",
            content,
            re.IGNORECASE,
        )

        if match:

            title = match.group(
                1
            )

        return Document(
            title=title,
            content=content,
        )