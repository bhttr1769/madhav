from brain.ui.detectors.fake_ui_element_detector import (
    FakeUIElementDetector,
)

from brain.ui.detectors.ui_element_detector import (
    UIElementDetector,
)

from brain.ui.models.screen import (
    Screen,
)

from brain.ui.models.ui_element import (
    UIElement,
)


def test_ui_element_detector_is_interface():

    assert (
        UIElementDetector.__abstractmethods__
        == {"detect"}
    )


def test_fake_detector_returns_elements():

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
    )

    detector = FakeUIElementDetector(
        frozenset({
            element,
        })
    )

    result = detector.detect(
        screen,
    )

    assert result == frozenset({
        element,
    })