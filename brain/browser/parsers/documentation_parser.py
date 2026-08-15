import re

from brain.browser.models.documentation import (
    Documentation,
)


class DocumentationParser:
    """
    Parses documentation sections.
    """

    def parse(
        self,
        text: str,
    ) -> Documentation:

        sections = re.findall(
            r"#+\s+(.*)",
            text,
        )

        return Documentation(
            sections=sections,
        )