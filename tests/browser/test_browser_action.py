import pytest

from brain.browser.interactive.models.browser_action import BrowserAction
from brain.browser.interactive.models.browser_element import BrowserElement


def test_browser_action_stores_values():
    element = BrowserElement(
        element_type="button",
        name="Submit",
        text="Submit",
        selector="button:nth-of-type(1)",
        interactive=True,
    )

    action = BrowserAction(
        action_type="click",
        target=element,
    )

    assert action.action_type == "click"
    assert action.target == element
    assert action.text is None
    assert action.key is None
    assert action.url is None


def test_browser_action_supports_type_action():
    element = BrowserElement(
        element_type="input",
        name="Username",
        text=None,
        selector="input:nth-of-type(1)",
        interactive=True,
    )

    action = BrowserAction(
        action_type="type",
        target=element,
        text="Parth",
    )

    assert action.action_type == "type"
    assert action.target == element
    assert action.text == "Parth"


def test_browser_action_supports_press_action():
    element = BrowserElement(
        element_type="input",
        name="Search",
        text=None,
        selector="input:nth-of-type(1)",
        interactive=True,
    )

    action = BrowserAction(
        action_type="press",
        target=element,
        key="Enter",
    )

    assert action.action_type == "press"
    assert action.target == element
    assert action.key == "Enter"


def test_browser_action_supports_navigate_action():
    action = BrowserAction(
        action_type="navigate",
        url="https://example.com",
    )

    assert action.action_type == "navigate"
    assert action.url == "https://example.com"
    assert action.target is None


def test_browser_action_is_immutable():
    action = BrowserAction(
        action_type="click",
    )

    with pytest.raises(AttributeError):
        action.action_type = "type"