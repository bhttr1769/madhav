from brain.browser.cleaners.text_cleaner import (
    TextCleaner,
)

from brain.browser.registries.cleaner_registry import (
    CleanerRegistry,
)


def test_cleaner_registry():

    registry = (
        CleanerRegistry()
    )

    registry.register(
        TextCleaner(),
    )

    assert (
        len(
            registry.all()
        )
        == 1
    )