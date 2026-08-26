from brain.ui.detectors.ui_element_detector import (
    UIElementDetector,
)

from brain.ui.models.screen import (
    Screen,
)

from brain.ui.models.ui_element import (
    UIElement,
)


class FakeUIElementDetector(
    UIElementDetector,
):
    """
    Deterministic UI-element detector for testing.
    """

    def __init__(
        self,
        elements: frozenset[UIElement],
    ):
        self._elements = elements

    def detect(
        self,
        screen: Screen,
    ) -> frozenset[UIElement]:

        return self._elements