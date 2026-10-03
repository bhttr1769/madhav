from dataclasses import dataclass


@dataclass(frozen=True)
class BrowserElement:
    """
    Represents an observable web element in the current browser page.
    """

    element_type: str
    name: str | None
    text: str | None
    selector: str
    interactive: bool