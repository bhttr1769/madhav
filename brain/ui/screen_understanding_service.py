from brain.ui.capture.screen_capture import (
    ScreenCapture,
)

from brain.ui.detectors.ui_element_detector import (
    UIElementDetector,
)

from brain.ui.models.screen_understanding import (
    ScreenUnderstanding,
)


class ScreenUnderstandingService:
    """
    Orchestrates screen capture and UI-element detection.
    """

    def __init__(
        self,
        capture: ScreenCapture,
        detector: UIElementDetector,
    ):

        self._capture = capture
        self._detector = detector

    def understand(
        self,
    ) -> ScreenUnderstanding:

        screen = self._capture.capture()

        elements = self._detector.detect(
            screen,
        )

        return ScreenUnderstanding(
            screen=screen,
            elements=elements,
            application=None,
            window_title=None,
        )