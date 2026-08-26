from dataclasses import dataclass

from brain.ui.models.screen import (
    Screen,
)

from brain.ui.models.ui_element import (
    UIElement,
)


@dataclass(frozen=True)
class ScreenUnderstanding:
    """
    Represents interpreted screen information.
    """

    screen: Screen

    elements: frozenset[UIElement]

    application: str | None

    window_title: str | None