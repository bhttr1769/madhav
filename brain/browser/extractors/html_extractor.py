import re

from brain.browser.extractors.base_extractor import (
    BaseExtractor,
)

from brain.browser.models.extracted_content import (
    ExtractedContent,
)


class HtmlExtractor(
    BaseExtractor,
):

    def can_extract(
        self,
        document,
    ) -> bool:

        return bool(
            document.content,
        )

    def extract(
        self,
        document,
    ) -> ExtractedContent:

        text = re.sub(
            r"<[^>]+>",
            " ",
            document.content,
        )

        return ExtractedContent(
            text=text,
        )