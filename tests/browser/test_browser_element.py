import pytest

from brain.browser.interactive.models.browser_element import (
    BrowserElement,
)


def test_browser_element_stores_values():
    element = BrowserElement(
        element_type="button",
        name="Submit",
        text="Submit",
        selector="button:nth-of-type(1)",
        interactive=True,
    )

    assert element.element_type == "button"
    assert element.name == "Submit"
    assert element.text == "Submit"
    assert element.selector == "button:nth-of-type(1)"
    assert element.interactive is True


def test_browser_element_is_immutable():
    element = BrowserElement(
        element_type="button",
        name="Submit",
        text="Submit",
        selector="button:nth-of-type(1)",
        interactive=True,
    )

    with pytest.raises(AttributeError):
        element.text = "Changed"