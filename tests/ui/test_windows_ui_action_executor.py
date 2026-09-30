from brain.ui.executors.windows_ui_action_executor import (
    WindowsUIActionExecutor,
)

from brain.ui.models.ui_action import (
    UIAction,
)

from brain.ui.models.ui_element import (
    UIElement,
)


class FakeWindowsInput:

    def __init__(self):
        self.calls = []

    def move(self, x, y):
        self.calls.append(
            ("move", x, y)
        )

    def click(self):
        self.calls.append(
            ("click",)
        )

    def double_click(self):
        self.calls.append(
            ("double_click",)
        )

    def type_text(self, text):
        self.calls.append(
            ("type", text)
        )

    def press(self, key):
        self.calls.append(
            ("press", key)
        )


def create_button():

    return UIElement(
        element_type="button",
        name="Submit",
        x=100,
        y=200,
        width=120,
        height=40,
    )


def test_click_element():

    fake = FakeWindowsInput()

    executor = WindowsUIActionExecutor(
        fake
    )

    executor.execute(
        UIAction(
            action_type="click",
            target=create_button(),
        )
    )

    assert fake.calls == [
        ("move", 160, 220),
        ("click",),
    ]


def test_click_coordinates():

    fake = FakeWindowsInput()

    executor = WindowsUIActionExecutor(
        fake
    )

    executor.execute(
        UIAction(
            action_type="click",
            x=500,
            y=300,
        )
    )

    assert fake.calls == [
        ("move", 500, 300),
        ("click",),
    ]


def test_double_click():

    fake = FakeWindowsInput()

    executor = WindowsUIActionExecutor(
        fake
    )

    executor.execute(
        UIAction(
            action_type="double_click",
            x=500,
            y=300,
        )
    )

    assert fake.calls == [
        ("move", 500, 300),
        ("double_click",),
    ]


def test_move():

    fake = FakeWindowsInput()

    executor = WindowsUIActionExecutor(
        fake
    )

    executor.execute(
        UIAction(
            action_type="move",
            x=500,
            y=300,
        )
    )

    assert fake.calls == [
        ("move", 500, 300),
    ]


def test_type():

    fake = FakeWindowsInput()

    executor = WindowsUIActionExecutor(
        fake
    )

    executor.execute(
        UIAction(
            action_type="type",
            text="hello",
        )
    )

    assert fake.calls == [
        ("type", "hello"),
    ]


def test_press():

    fake = FakeWindowsInput()

    executor = WindowsUIActionExecutor(
        fake
    )

    executor.execute(
        UIAction(
            action_type="press",
            key="ENTER",
        )
    )

    assert fake.calls == [
        ("press", "ENTER"),
    ]


def test_invalid_action_type_is_rejected():

    fake = FakeWindowsInput()

    executor = WindowsUIActionExecutor(
        fake
    )

    action = object.__new__(
        UIAction
    )

    object.__setattr__(
        action,
        "action_type",
        "invalid",
    )

    object.__setattr__(
        action,
        "target",
        None,
    )

    object.__setattr__(
        action,
        "x",
        None,
    )

    object.__setattr__(
        action,
        "y",
        None,
    )

    object.__setattr__(
        action,
        "text",
        None,
    )

    object.__setattr__(
        action,
        "key",
        None,
    )

    try:
        executor.execute(action)
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Expected ValueError"
        )