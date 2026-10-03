from unittest.mock import MagicMock

import pytest

from brain.browser.interactive.browser_session import BrowserSession
from brain.browser.interactive.models.browser_action import BrowserAction
from brain.browser.interactive.models.browser_element import BrowserElement
from brain.browser.interactive.models.browser_observation import (
    BrowserObservation,
)
from brain.browser.interactive.models.browser_session_state import (
    BrowserSessionState,
)
from brain.browser.interactive.playwright_browser_executor import (
    PlaywrightBrowserExecutor,
)


class FakeBrowserSession(BrowserSession):
    def __init__(self):
        self._page = MagicMock()
        self._navigate_mock = MagicMock()

    def start(self) -> None:
        pass

    def close(self) -> None:
        pass

    def navigate(self, url: str) -> None:
        self._navigate_mock(url)

    def current_state(self) -> BrowserSessionState:
        return BrowserSessionState(
            active=self._page is not None,
            url="https://example.com",
        )

    def observe(self) -> BrowserObservation:
        raise NotImplementedError


def create_element(
    element_type="button",
    selector="button:nth-of-type(1)",
):
    return BrowserElement(
        element_type=element_type,
        name="Test",
        text="Test",
        selector=selector,
        interactive=True,
    )


def create_session():
    session = FakeBrowserSession()
    locator = MagicMock()
    session._page.locator.return_value = locator
    return session, locator


def test_click_action():
    session, locator = create_session()

    executor = PlaywrightBrowserExecutor(session)

    action = BrowserAction(
        action_type="click",
        target=create_element(),
    )

    executor.execute(action)

    session._page.locator.assert_called_once_with(
        "button:nth-of-type(1)"
    )
    locator.click.assert_called_once_with()


def test_type_action():
    session, locator = create_session()

    executor = PlaywrightBrowserExecutor(session)

    action = BrowserAction(
        action_type="type",
        target=create_element(
            element_type="input",
            selector="input:nth-of-type(1)",
        ),
        text="Parth",
    )

    executor.execute(action)

    session._page.locator.assert_called_once_with(
        "input:nth-of-type(1)"
    )
    locator.fill.assert_called_once_with("Parth")


def test_press_action():
    session, locator = create_session()

    executor = PlaywrightBrowserExecutor(session)

    action = BrowserAction(
        action_type="press",
        target=create_element(
            element_type="input",
            selector="input:nth-of-type(1)",
        ),
        key="Enter",
    )

    executor.execute(action)

    session._page.locator.assert_called_once_with(
        "input:nth-of-type(1)"
    )
    locator.press.assert_called_once_with("Enter")


def test_navigate_action():
    session, _ = create_session()

    executor = PlaywrightBrowserExecutor(session)

    action = BrowserAction(
        action_type="navigate",
        url="https://example.com",
    )

    executor.execute(action)

    session._navigate_mock.assert_called_once_with(
    "https://example.com"
)


def test_execution_requires_active_session():
    session = FakeBrowserSession()
    session._page = None

    executor = PlaywrightBrowserExecutor(session)

    action = BrowserAction(
        action_type="click",
        target=create_element(),
    )

    with pytest.raises(RuntimeError, match="not active"):
        executor.execute(action)


def test_invalid_action_type_is_rejected():
    session, _ = create_session()

    executor = PlaywrightBrowserExecutor(session)

    action = BrowserAction(
        action_type="delete",
        target=create_element(),
    )

    with pytest.raises(
        ValueError,
        match="unsupported browser action: delete",
    ):
        executor.execute(action)


def test_type_requires_text():
    session, _ = create_session()

    executor = PlaywrightBrowserExecutor(session)

    action = BrowserAction(
        action_type="type",
        target=create_element(
            element_type="input",
            selector="input:nth-of-type(1)",
        ),
    )

    with pytest.raises(ValueError, match="requires text"):
        executor.execute(action)


def test_press_requires_key():
    session, _ = create_session()

    executor = PlaywrightBrowserExecutor(session)

    action = BrowserAction(
        action_type="press",
        target=create_element(
            element_type="input",
            selector="input:nth-of-type(1)",
        ),
    )

    with pytest.raises(ValueError, match="requires key"):
        executor.execute(action)


def test_navigate_requires_url():
    session, _ = create_session()

    executor = PlaywrightBrowserExecutor(session)

    action = BrowserAction(
        action_type="navigate",
    )

    with pytest.raises(ValueError, match="requires a url"):
        executor.execute(action)