from dataclasses import dataclass

from brain.browser.interactive.models.browser_element import (
    BrowserElement,
)


@dataclass(frozen=True)
class BrowserObservation:
    """
    Represents the currently observed browser page.
    """

    url: str | None
    title: str | None
    text: str | None
    elements: frozenset[BrowserElement] = frozenset()