from brain.ui.models.screen import (
    Screen,
)

from brain.ui.models.screen_understanding import (
    ScreenUnderstanding,
)

from brain.ui.models.ui_element import (
    UIElement,
)


def test_screen_model():

    screen = Screen(
        width=1920,
        height=1080,
        image_path="screen.png",
    )

    assert screen.width == 1920
    assert screen.height == 1080
    assert screen.image_path == "screen.png"


def test_ui_element_model():

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

    assert element.element_type == "button"
    assert element.name == "Submit"
    assert element.x == 100
    assert element.y == 200
    assert element.width == 120
    assert element.height == 40
    assert element.text == "Submit"
    assert element.confidence == 0.95


def test_screen_understanding():

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

    understanding = ScreenUnderstanding(
        screen=screen,
        elements=frozenset({
            element,
        }),
        application="Example",
        window_title="Example Window",
    )

    assert understanding.screen == screen
    assert element in understanding.elements
    assert understanding.application == "Example"
    assert understanding.window_title == (
        "Example Window"
    )