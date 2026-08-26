from brain.ui.capture.fake_screen_capture import (
    FakeScreenCapture,
)

from brain.ui.detectors.fake_ui_element_detector import (
    FakeUIElementDetector,
)

from brain.ui.models.screen import (
    Screen,
)

from brain.ui.models.ui_element import (
    UIElement,
)

from brain.ui.screen_understanding_service import (
    ScreenUnderstandingService,
)


def test_screen_understanding_service_captures_screen():

    screen = Screen(
        width=1920,
        height=1080,
        image_path="screen.png",
    )

    capture = FakeScreenCapture(
        screen,
    )

    detector = FakeUIElementDetector(
        frozenset(),
    )

    service = ScreenUnderstandingService(
        capture=capture,
        detector=detector,
    )

    result = service.understand()

    assert result.screen == screen


def test_screen_understanding_service_detects_elements():

    screen = Screen(
        width=1920,
        height=1080,
    )

    element = UIElement(
        element_type="button",
        name="Submit",
        x=100,
        y=200,
        width=120,
        height=40,
        text="Submit",
        confidence=0.95,
    )

    capture = FakeScreenCapture(
        screen,
    )

    detector = FakeUIElementDetector(
        frozenset({
            element,
        }),
    )

    service = ScreenUnderstandingService(
        capture=capture,
        detector=detector,
    )

    result = service.understand()

    assert result.elements == frozenset({
        element,
    })


def test_screen_understanding_service_preserves_screen():

    screen = Screen(
        width=1366,
        height=768,
        image_path="desktop.png",
    )

    capture = FakeScreenCapture(
        screen,
    )

    detector = FakeUIElementDetector(
        frozenset(),
    )

    service = ScreenUnderstandingService(
        capture=capture,
        detector=detector,
    )

    result = service.understand()

    assert result.screen.width == 1366
    assert result.screen.height == 768
    assert result.screen.image_path == (
        "desktop.png"
    )


def test_screen_understanding_service_defaults_window_context():

    screen = Screen(
        width=1920,
        height=1080,
    )

    capture = FakeScreenCapture(
        screen,
    )

    detector = FakeUIElementDetector(
        frozenset(),
    )

    service = ScreenUnderstandingService(
        capture=capture,
        detector=detector,
    )

    result = service.understand()

    assert result.application is None
    assert result.window_title is None


def test_screen_understanding_service_handles_no_elements():

    screen = Screen(
        width=1920,
        height=1080,
    )

    capture = FakeScreenCapture(
        screen,
    )

    detector = FakeUIElementDetector(
        frozenset(),
    )

    service = ScreenUnderstandingService(
        capture=capture,
        detector=detector,
    )

    result = service.understand()

    assert result.elements == frozenset()