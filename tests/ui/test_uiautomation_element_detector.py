from unittest.mock import Mock

import pytest

from brain.ui.detectors.uiautomation_element_detector import (
    UIAutomationElementDetector,
)

from brain.ui.models.screen import (
    Screen,
)

from brain.ui.models.ui_element import (
    UIElement,
)


def test_detector_requires_integer_depth():

    with pytest.raises(TypeError):
        UIAutomationElementDetector(
            max_depth="8",
        )


def test_detector_rejects_negative_depth():

    with pytest.raises(ValueError):
        UIAutomationElementDetector(
            max_depth=-1,
        )


def test_detector_requires_screen():

    detector = UIAutomationElementDetector()

    with pytest.raises(TypeError):
        detector.detect(
            "screen",
        )


def test_detector_maps_control_to_ui_element():

    detector = UIAutomationElementDetector()

    control = Mock()

    control.BoundingRectangle = (
        100,
        200,
        220,
        240,
    )

    control.ControlTypeName = "ButtonControl"
    control.Name = "Submit"

    element = detector._to_element(
        control,
    )

    assert element == UIElement(
        element_type="ButtonControl",
        name="Submit",
        x=100,
        y=200,
        width=120,
        height=40,
        text="Submit",
        confidence=1.0,
    )


def test_detector_ignores_invalid_rectangle():

    detector = UIAutomationElementDetector()

    control = Mock()

    control.BoundingRectangle = (
        100,
        200,
        100,
        240,
    )

    control.ControlTypeName = "ButtonControl"
    control.Name = "Submit"

    assert detector._to_element(
        control,
    ) is None


def test_detector_respects_max_depth():

    detector = UIAutomationElementDetector(
        max_depth=0,
    )

    root = Mock()
    root.BoundingRectangle = (
        0,
        0,
        100,
        100,
    )
    root.ControlTypeName = "WindowControl"
    root.Name = "Test"

    child = Mock()
    child.BoundingRectangle = (
        10,
        10,
        50,
        50,
    )
    child.ControlTypeName = "ButtonControl"
    child.Name = "Child"

    root.GetChildren.return_value = [
        child,
    ]

    elements = []

    detector._collect(
        control=root,
        elements=elements,
        depth=0,
    )

    assert elements == [
        UIElement(
            element_type="WindowControl",
            name="Test",
            x=0,
            y=0,
            width=100,
            height=100,
            text="Test",
            confidence=1.0,
        )
    ]