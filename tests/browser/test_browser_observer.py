import pytest

from brain.browser.interactive.browser_observer import (
    BrowserObserver,
)
from brain.browser.interactive.models.browser_observation import (
    BrowserObservation,
)

from brain.browser.interactive.models.browser_element import (
    BrowserElement,
)


def test_browser_observer_is_interface():
    assert BrowserObserver.__abstractmethods__ == {
        "observe",
    }


def test_browser_observation_is_immutable():
    observation = BrowserObservation(
        url="https://example.com",
        title="Example",
        text="Example Domain",
    )

    with pytest.raises(
        AttributeError
    ):
        observation.title = "Changed"


def test_browser_observation_stores_page_state():
    observation = BrowserObservation(
        url="https://example.com",
        title="Example",
        text="Example Domain",
    )

    assert observation.url == "https://example.com"
    assert observation.title == "Example"
    assert observation.text == "Example Domain"

def test_browser_observation_stores_elements():
    element = BrowserElement(
        element_type="button",
        name="Submit",
        text="Submit",
        selector="button:nth-of-type(1)",
        interactive=True,
    )

    observation = BrowserObservation(
        url="https://example.com",
        title="Example",
        text="Example Domain",
        elements=frozenset({element}),
    )

    assert observation.elements == frozenset({element})