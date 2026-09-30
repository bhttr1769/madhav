import uiautomation as auto

from brain.ui.detectors.ui_element_detector import (
    UIElementDetector,
)

from brain.ui.models.screen import (
    Screen,
)

from brain.ui.models.ui_element import (
    UIElement,
)


class UIAutomationElementDetector(
    UIElementDetector,
):
    """
    Detects UI elements from the focused window
    using Windows UI Automation.
    """

    def __init__(
        self,
        max_depth: int = 8,
    ):
        if not isinstance(max_depth, int):
            raise TypeError(
                "max_depth must be an integer"
            )

        if max_depth < 0:
            raise ValueError(
                "max_depth must be non-negative"
            )

        self._max_depth = max_depth

    def detect(
        self,
        screen: Screen,
    ) -> frozenset[UIElement]:

        if not isinstance(screen, Screen):
            raise TypeError(
                "screen must be a Screen"
            )

        focused = auto.GetFocusedControl()

        if focused is None:
            return frozenset()

        elements = []

        self._collect(
            control=focused,
            elements=elements,
            depth=0,
        )

        return frozenset(elements)

    def _collect(
        self,
        control,
        elements: list[UIElement],
        depth: int,
    ) -> None:

        if depth > self._max_depth:
            return

        element = self._to_element(
            control,
        )

        if element is not None:
            elements.append(element)

        if depth == self._max_depth:
            return

        children = control.GetChildren()

        for child in children:
            self._collect(
                control=child,
                elements=elements,
                depth=depth + 1,
            )

    def _to_element(
        self,
        control,
    ) -> UIElement | None:

        rectangle = control.BoundingRectangle

        if rectangle is None:
            return None

        left, top, right, bottom = rectangle

        x = left
        y = top
        width = right - left
        height = bottom - top

        if width <= 0 or height <= 0:
            return None

        element_type = (
            getattr(
                control,
                "ControlTypeName",
                None,
            )
            or "unknown"
        )

        name = (
            getattr(
                control,
                "Name",
                None,
            )
            or ""
        )

        text = self._extract_text(
            control,
        )

        return UIElement(
            element_type=element_type,
            name=name,
            x=x,
            y=y,
            width=width,
            height=height,
            text=text,
            confidence=1.0,
        )

    def _extract_text(
        self,
        control,
    ) -> str | None:

        name = getattr(
            control,
            "Name",
            None,
        )

        if isinstance(name, str) and name.strip():
            return name

        return None