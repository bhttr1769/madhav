from brain.ui.capture.fake_screen_capture import (
    FakeScreenCapture,
)

from brain.ui.capture.screen_capture import (
    ScreenCapture,
)

from brain.ui.models.screen import (
    Screen,
)


def test_screen_capture_is_interface():

    assert ScreenCapture.__abstractmethods__ == {
        "capture",
    }


def test_fake_screen_capture_returns_screen():

    screen = Screen(
        width=1920,
        height=1080,
        image_path="screen.png",
    )

    capture = FakeScreenCapture(
        screen,
    )

    result = capture.capture()

    assert result == screen