import pytest

from brain.safety.models.action import (
    Action,
)

from brain.ui.models.ui_action import (
    UIAction,
)

from brain.ui.models.ui_element import (
    UIElement,
)


def create_button():
    return UIElement(
        element_type="button",
        name="Submit",
        x=100,
        y=200,
        width=120,
        height=40,
        text="Submit",
    )


def test_click_action_with_target():

    element = create_button()

    action = UIAction(
        action_type="click",
        target=element,
    )

    assert action.action_type == "click"
    assert action.target == element


def test_click_action_with_coordinates():

    action = UIAction(
        action_type="click",
        x=500,
        y=300,
    )

    assert action.action_type == "click"
    assert action.x == 500
    assert action.y == 300


def test_double_click_action():

    element = create_button()

    action = UIAction(
        action_type="double_click",
        target=element,
    )

    assert action.action_type == "double_click"
    assert action.target == element


def test_move_action():

    action = UIAction(
        action_type="move",
        x=500,
        y=300,
    )

    assert action.action_type == "move"
    assert action.x == 500
    assert action.y == 300


def test_type_action():

    action = UIAction(
        action_type="type",
        text="hello",
    )

    assert action.action_type == "type"
    assert action.text == "hello"


def test_press_action():

    action = UIAction(
        action_type="press",
        key="ENTER",
    )

    assert action.action_type == "press"
    assert action.key == "ENTER"


def test_ui_action_is_immutable():

    action = UIAction(
        action_type="click",
        x=100,
        y=200,
    )

    with pytest.raises(
        AttributeError,
    ):
        action.x = 500


def test_invalid_action_type():

    with pytest.raises(
        ValueError,
        match="unsupported UI action type",
    ):
        UIAction(
            action_type="launch",
            x=100,
            y=200,
        )


def test_click_requires_target_or_coordinates():

    with pytest.raises(
        ValueError,
        match="requires a target",
    ):
        UIAction(
            action_type="click",
        )


def test_double_click_requires_target_or_coordinates():

    with pytest.raises(
        ValueError,
        match="requires a target",
    ):
        UIAction(
            action_type="double_click",
        )


def test_move_requires_target_or_coordinates():

    with pytest.raises(
        ValueError,
        match="requires a target",
    ):
        UIAction(
            action_type="move",
        )


def test_type_requires_text():

    with pytest.raises(
        ValueError,
        match="requires text",
    ):
        UIAction(
            action_type="type",
        )


def test_press_requires_key():

    with pytest.raises(
        ValueError,
        match="requires key",
    ):
        UIAction(
            action_type="press",
        )


def test_target_must_be_ui_element():

    with pytest.raises(
        TypeError,
        match="target must be a UIElement",
    ):
        UIAction(
            action_type="click",
            target="Submit",
        )


def test_coordinates_must_be_integers():

    with pytest.raises(
        TypeError,
        match="x must be an integer",
    ):
        UIAction(
            action_type="click",
            x=10.5,
            y=20,
        )


def test_text_must_be_string():

    with pytest.raises(
        TypeError,
        match="text must be a string",
    ):
        UIAction(
            action_type="type",
            text=123,
        )


def test_key_must_be_string():

    with pytest.raises(
        TypeError,
        match="key must be a string",
    ):
        UIAction(
            action_type="press",
            key=13,
        )


def test_click_converts_to_safety_action():

    element = create_button()

    ui_action = UIAction(
        action_type="click",
        target=element,
    )

    action = ui_action.to_action()

    assert isinstance(
        action,
        Action,
    )

    assert action.name == "click"
    assert action.category == "ui"

    assert action.target == (
        "element=button:Submit;"
        "bounds=100,200,120,40"
    )


def test_coordinate_click_converts_to_safety_action():

    ui_action = UIAction(
        action_type="click",
        x=500,
        y=300,
    )

    action = ui_action.to_action()

    assert action == Action(
        name="click",
        category="ui",
        target="x=500;y=300",
    )


def test_type_converts_to_safety_action():

    ui_action = UIAction(
        action_type="type",
        text="hello",
    )

    action = ui_action.to_action()

    assert action == Action(
        name="type",
        category="ui",
        target="text='hello'",
    )


def test_press_converts_to_safety_action():

    ui_action = UIAction(
        action_type="press",
        key="ENTER",
    )

    action = ui_action.to_action()

    assert action == Action(
        name="press",
        category="ui",
        target="key=ENTER",
    )