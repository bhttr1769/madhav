from brain.browser.interactive.browser_observation_builder import (
    BrowserObservationBuilder,
)
from brain.browser.interactive.models.browser_element import BrowserElement
from brain.browser.interactive.models.browser_observation import (
    BrowserObservation,
)
from brain.perception.models.observation import Observation
import pytest


def test_builds_page_observations():
    observation = BrowserObservation(
        url="https://example.com",
        title="Example",
        text="Example page",
    )

    result = BrowserObservationBuilder().build(
        observation
    )

    assert Observation(
        source="browser",
        category="url",
        subject="page",
        value="https://example.com",
    ) in result

    assert Observation(
        source="browser",
        category="title",
        subject="page",
        value="Example",
    ) in result

    assert Observation(
        source="browser",
        category="text",
        subject="page",
        value="Example page",
    ) in result


def test_builds_element_observations():
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
        text="Submit",
        elements=frozenset({element}),
    )

    result = BrowserObservationBuilder().build(
        observation
    )

    assert Observation(
        source="browser",
        category="element",
        subject="button:nth-of-type(1)",
        value="button",
    ) in result

    assert Observation(
        source="browser",
        category="element_name",
        subject="button:nth-of-type(1)",
        value="Submit",
    ) in result

    assert Observation(
        source="browser",
        category="element_text",
        subject="button:nth-of-type(1)",
        value="Submit",
    ) in result

    assert Observation(
        source="browser",
        category="interactive",
        subject="button:nth-of-type(1)",
        value="True",
    ) in result


def test_empty_browser_observation_produces_empty_result():
    observation = BrowserObservation(
        url=None,
        title=None,
        text=None,
        elements=frozenset(),
    )

    result = BrowserObservationBuilder().build(
        observation
    )

    assert result == frozenset()


def test_invalid_observation_is_rejected():
    with pytest.raises(
        TypeError,
        match="observation must be a BrowserObservation",
    ):
        BrowserObservationBuilder().build(
            object()
        )