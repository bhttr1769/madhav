from brain.ui.capture.screen_capture import ScreenCapture
from brain.ui.detectors.ui_element_detector import UIElementDetector

from brain.ui.context.ui_context_resolver import (
    UIContextResolver,
    WindowsUIContextResolver,
)
from brain.ui.models.screen import Screen
from brain.ui.models.screen_understanding import (
    ScreenUnderstanding,
)
from brain.ui.screen_understanding_service import (
    ScreenUnderstandingService,
)


class FakeControlType:
    WindowControl = "window"


class FakeAutomation:
    ControlType = FakeControlType()


class FakeControl:
    def __init__(
        self,
        name="",
        control_type=None,
        process_id=None,
        parent=None,
    ):
        self.Name = name
        self.ControlType = control_type
        self.ProcessId = process_id
        self._parent = parent

    def GetParentControl(self):
        return self._parent


class FakeAutomationWithFocusedControl(
    FakeAutomation,
):

    def __init__(
        self,
        focused_control,
    ):
        self._focused_control = (
            focused_control
        )

    def GetFocusedControl(self):
        return self._focused_control


class FakeCapture(ScreenCapture):

    def capture(self):
        return Screen(
            width=1920,
            height=1080,
        )


class FakeDetector(UIElementDetector):

    def detect(self, screen):
        return frozenset()


class FakeContextResolver(
    UIContextResolver,
):

    def __init__(
        self,
        application,
        window_title,
    ):
        self._application = application
        self._window_title = window_title

    def resolve(self):
        return (
            self._application,
            self._window_title,
        )


def test_resolver_returns_window_title_and_application(
    monkeypatch,
):

    window = FakeControl(
        name="Test Window",
        control_type="window",
        process_id=1234,
    )

    focused = FakeControl(
        name="Focused Control",
        control_type="text",
        process_id=1234,
        parent=window,
    )

    automation = FakeAutomationWithFocusedControl(
        focused
    )

    monkeypatch.setattr(
        WindowsUIContextResolver,
        "_resolve_process_name",
        staticmethod(
            lambda process_id: "test.exe"
        ),
    )

    resolver = WindowsUIContextResolver(
        automation=automation,
    )

    application, window_title = (
        resolver.resolve()
    )

    assert application == "test.exe"
    assert window_title == "Test Window"


def test_resolver_finds_window_ancestor():

    window = FakeControl(
        name="Application Window",
        control_type="window",
    )

    intermediate = FakeControl(
        control_type="pane",
        parent=window,
    )

    focused = FakeControl(
        control_type="text",
        parent=intermediate,
    )

    automation = FakeAutomationWithFocusedControl(
        focused
    )

    resolver = WindowsUIContextResolver(
        automation=automation,
    )

    resolved_window = (
        resolver._find_window_ancestor(
            focused
        )
    )

    assert resolved_window is window


def test_resolver_returns_none_when_no_focused_control():

    automation = (
        FakeAutomationWithFocusedControl(
            None
        )
    )

    resolver = WindowsUIContextResolver(
        automation=automation,
    )

    assert resolver.resolve() == (
        None,
        None,
    )


def test_resolver_returns_none_when_no_window_ancestor():

    focused = FakeControl(
        name="Focused Control",
        control_type="text",
        process_id=1234,
    )

    automation = FakeAutomationWithFocusedControl(
        focused
    )

    resolver = WindowsUIContextResolver(
        automation=automation,
    )

    assert resolver.resolve() == (
        None,
        None,
    )


def test_resolver_returns_none_when_process_cannot_be_resolved(
    monkeypatch,
):

    window = FakeControl(
        name="Test Window",
        control_type="window",
        process_id=1234,
    )

    focused = FakeControl(
        control_type="text",
        process_id=1234,
        parent=window,
    )

    automation = FakeAutomationWithFocusedControl(
        focused
    )

    monkeypatch.setattr(
        WindowsUIContextResolver,
        "_resolve_process_name",
        staticmethod(
            lambda process_id: None
        ),
    )

    resolver = WindowsUIContextResolver(
        automation=automation,
    )

    application, window_title = (
        resolver.resolve()
    )

    assert application is None
    assert window_title == "Test Window"


def test_screen_understanding_service_uses_context_resolver():

    resolver = FakeContextResolver(
        application="TestApp.exe",
        window_title="Test Window",
    )

    service = ScreenUnderstandingService(
        capture=FakeCapture(),
        detector=FakeDetector(),
        context_resolver=resolver,
    )

    result = service.understand()

    assert isinstance(
        result,
        ScreenUnderstanding,
    )

    assert result.application == (
        "TestApp.exe"
    )

    assert result.window_title == (
        "Test Window"
    )


def test_screen_understanding_service_preserves_detected_elements():

    class Detector(FakeDetector):

        def detect(self, screen):
            return frozenset()

    resolver = FakeContextResolver(
        application="TestApp.exe",
        window_title="Test Window",
    )

    service = ScreenUnderstandingService(
        capture=FakeCapture(),
        detector=Detector(),
        context_resolver=resolver,
    )

    result = service.understand()

    assert result.elements == frozenset()


def test_context_resolver_requires_correct_type():

    try:
        ScreenUnderstandingService(
            capture=FakeCapture(),
            detector=FakeDetector(),
            context_resolver=object(),
        )

        assert False

    except TypeError as error:

        assert str(error) == (
            "context_resolver must be a UIContextResolver"
        )