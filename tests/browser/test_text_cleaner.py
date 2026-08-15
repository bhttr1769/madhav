from brain.browser.models.extracted_content import (
    ExtractedContent,
)

from brain.browser.cleaners.text_cleaner import (
    TextCleaner,
)


def test_text_cleaner():

    extracted = (
        ExtractedContent(
            text=" Hello \n\n World \t "
        )
    )

    cleaned = (
        TextCleaner()
    ).clean(
        extracted,
    )

    assert (
        cleaned.text
        == "Hello World"
    )