import re

from brain.browser.cleaners.base_cleaner import (
    BaseCleaner,
)

from brain.browser.models.clean_content import (
    CleanContent,
)


class TextCleaner(
    BaseCleaner,
):

    def can_clean(
        self,
        extracted_content,
    ) -> bool:

        return bool(
            extracted_content.text,
        )

    def clean(
        self,
        extracted_content,
    ) -> CleanContent:

        text = re.sub(
            r"\s+",
            " ",
            extracted_content.text,
        )

        return CleanContent(
            text=text.strip(),
        )