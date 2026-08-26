from brain.ui.capture.screen_capture import (
    ScreenCapture,
)

from brain.ui.models.screen import (
    Screen,
)


class FakeScreenCapture(
    ScreenCapture,
):
    """
    Deterministic screen-capture implementation
    for testing.
    """

    def __init__(
        self,
        screen: Screen,
    ):
        self._screen = screen

    def capture(self) -> Screen:
        return self._screen