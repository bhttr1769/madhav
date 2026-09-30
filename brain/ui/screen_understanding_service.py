from brain.ui.capture.screen_capture import (
    ScreenCapture,
)

from brain.ui.context.ui_context_resolver import (
    UIContextResolver,
    WindowsUIContextResolver,
)

from brain.ui.detectors.ui_element_detector import (
    UIElementDetector,
)

from brain.ui.models.screen_understanding import (
    ScreenUnderstanding,
)


class ScreenUnderstandingService:
    """
    Orchestrates screen capture, UI-element detection,
    and application/window context resolution.
    """

    def __init__(
        self,
        capture: ScreenCapture,
        detector: UIElementDetector,
        context_resolver: UIContextResolver | None = None,
    ):

        if not isinstance(
            capture,
            ScreenCapture,
        ):
            raise TypeError(
                "capture must be a ScreenCapture"
            )

        if not isinstance(
            detector,
            UIElementDetector,
        ):
            raise TypeError(
                "detector must be a UIElementDetector"
            )

        if (
            context_resolver is not None
            and not isinstance(
                context_resolver,
                UIContextResolver,
            )
        ):
            raise TypeError(
                "context_resolver must be a UIContextResolver"
            )

        self._capture = capture
        self._detector = detector

        self._context_resolver = (
            context_resolver
            if context_resolver is not None
            else WindowsUIContextResolver()
        )

    def understand(
        self,
    ) -> ScreenUnderstanding:

        screen = self._capture.capture()

        elements = self._detector.detect(
            screen,
        )

        application, window_title = (
            self._context_resolver.resolve()
        )

        return ScreenUnderstanding(
            screen=screen,
            elements=elements,
            application=application,
            window_title=window_title,
        )