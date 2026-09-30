from brain.perception.models.observation import Observation
from brain.perception.ui_observation_builder import UIObservationBuilder
from brain.ui.models.screen import Screen
from brain.ui.models.screen_understanding import ScreenUnderstanding
from brain.ui.models.ui_element import UIElement


def create_understanding():
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

    return ScreenUnderstanding(
        screen=screen,
        elements=frozenset({element}),
        application="TestApp",
        window_title="Test Window",
    )


def test_application_is_converted_to_observation():

    understanding = create_understanding()

    observations = UIObservationBuilder().build(
        understanding
    )

    assert Observation(
        source="ui",
        category="application",
        subject="screen",
        value="TestApp",
    ) in observations


def test_window_title_is_converted_to_observation():

    understanding = create_understanding()

    observations = UIObservationBuilder().build(
        understanding
    )

    assert Observation(
        source="ui",
        category="window",
        subject="screen",
        value="Test Window",
    ) in observations


def test_ui_element_is_converted_to_observation():

    understanding = create_understanding()

    observations = UIObservationBuilder().build(
        understanding
    )

    element_observations = {
        observation
        for observation in observations
        if observation.category == "element"
    }

    assert len(element_observations) == 1

    observation = next(
        iter(element_observations)
    )

    assert observation.source == "ui"
    assert observation.value == "button"
    assert observation.confidence == 0.95


def test_element_text_is_converted_to_observation():

    understanding = create_understanding()

    observations = UIObservationBuilder().build(
        understanding
    )

    assert any(
        observation.source == "ui"
        and observation.category == "text"
        and observation.value == "Submit"
        for observation in observations
    )


def test_multiple_elements_are_preserved():

    screen = Screen(
        width=1920,
        height=1080,
    )

    first = UIElement(
        element_type="button",
        name="One",
        x=10,
        y=10,
        width=50,
        height=30,
    )

    second = UIElement(
        element_type="button",
        name="Two",
        x=100,
        y=10,
        width=50,
        height=30,
    )

    understanding = ScreenUnderstanding(
        screen=screen,
        elements=frozenset({first, second}),
        application=None,
        window_title=None,
    )

    observations = UIObservationBuilder().build(
        understanding
    )

    element_observations = {
        observation
        for observation in observations
        if observation.category == "element"
    }

    assert len(element_observations) == 2


def test_invalid_input_is_rejected():

    builder = UIObservationBuilder()

    try:
        builder.build(object())
        assert False
    except TypeError as error:
        assert str(error) == (
            "understanding must be a ScreenUnderstanding"
        )