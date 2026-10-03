from unittest.mock import MagicMock, patch

import pytest

from brain.browser.interactive.playwright_browser_session import (
    PlaywrightBrowserSession,
)

from brain.browser.interactive.models.browser_element import (
    BrowserElement,
)
from brain.browser.interactive.models.browser_observation import (
    BrowserObservation,
)


class FakeUrlValidator:
    def normalize(self, url):
        return "https://normalized.example"

    def is_valid(self, url):
        return True


class InvalidUrlValidator:
    def normalize(self, url):
        return url

    def is_valid(self, url):
        return False


def test_rejects_missing_executable():
    with pytest.raises(ValueError):
        PlaywrightBrowserSession(
            "C:\\does-not-exist\\chrome.exe"
        )


def test_starts_and_closes_browser(tmp_path):
    executable = tmp_path / "chrome.exe"
    executable.write_text("fake")

    playwright = MagicMock()
    browser = MagicMock()
    page = MagicMock()

    playwright.chromium.launch.return_value = browser
    browser.new_page.return_value = page

    with patch(
        "brain.browser.interactive.playwright_browser_session.sync_playwright"
    ) as factory:

        factory.return_value.start.return_value = playwright

        session = PlaywrightBrowserSession(
            str(executable)
        )

        session.start()

        playwright.chromium.launch.assert_called_once_with(
            executable_path=str(executable)
        )
        browser.new_page.assert_called_once()

        session.close()

        browser.close.assert_called_once()
        playwright.stop.assert_called_once()


def test_navigation_requires_active_session(tmp_path):
    executable = tmp_path / "chrome.exe"
    executable.write_text("fake")

    session = PlaywrightBrowserSession(
        str(executable)
    )

    with pytest.raises(RuntimeError):
        session.navigate("https://example.com")


def test_navigation_updates_state(tmp_path):
    executable = tmp_path / "chrome.exe"
    executable.write_text("fake")

    playwright = MagicMock()
    browser = MagicMock()
    page = MagicMock()

    playwright.chromium.launch.return_value = browser
    browser.new_page.return_value = page

    page.url = "https://example.com"

    with patch(
        "brain.browser.interactive.playwright_browser_session.sync_playwright"
    ) as factory:

        factory.return_value.start.return_value = playwright

        session = PlaywrightBrowserSession(
            str(executable)
        )

        session.start()
        session.navigate("https://example.com")

        page.goto.assert_called_once_with(
            "https://example.com"
        )

        state = session.current_state()

        assert state.active is True
        assert state.url == "https://example.com"

        session.close()


def test_close_is_safe_when_not_started(tmp_path):
    executable = tmp_path / "chrome.exe"
    executable.write_text("fake")

    session = PlaywrightBrowserSession(
        str(executable)
    )

    session.close()

    assert session.current_state().active is False


def test_navigate_normalizes_url(tmp_path):
    executable = tmp_path / "chrome.exe"
    executable.write_text("fake")

    playwright = MagicMock()
    browser = MagicMock()
    page = MagicMock()

    playwright.chromium.launch.return_value = browser
    browser.new_page.return_value = page

    validator = FakeUrlValidator()

    with patch(
        "brain.browser.interactive.playwright_browser_session.sync_playwright"
    ) as factory:

        factory.return_value.start.return_value = playwright

        session = PlaywrightBrowserSession(
            executable_path=str(executable),
            url_validator=validator,
        )

        session.start()
        session.navigate("example.com")

        page.goto.assert_called_once_with(
            "https://normalized.example"
        )

        session.close()


def test_navigate_preserves_https_url(tmp_path):
    executable = tmp_path / "chrome.exe"
    executable.write_text("fake")

    playwright = MagicMock()
    browser = MagicMock()
    page = MagicMock()

    playwright.chromium.launch.return_value = browser
    browser.new_page.return_value = page

    validator = FakeUrlValidator()

    with patch(
        "brain.browser.interactive.playwright_browser_session.sync_playwright"
    ) as factory:

        factory.return_value.start.return_value = playwright

        session = PlaywrightBrowserSession(
            executable_path=str(executable),
            url_validator=validator,
        )

        session.start()
        session.navigate("https://example.com")

        page.goto.assert_called_once_with(
            "https://normalized.example"
        )

        session.close()


def test_navigate_normalizes_whitespace(tmp_path):
    executable = tmp_path / "chrome.exe"
    executable.write_text("fake")

    playwright = MagicMock()
    browser = MagicMock()
    page = MagicMock()

    playwright.chromium.launch.return_value = browser
    browser.new_page.return_value = page

    validator = FakeUrlValidator()

    with patch(
        "brain.browser.interactive.playwright_browser_session.sync_playwright"
    ) as factory:

        factory.return_value.start.return_value = playwright

        session = PlaywrightBrowserSession(
            executable_path=str(executable),
            url_validator=validator,
        )

        session.start()
        session.navigate("  example.com  ")

        page.goto.assert_called_once_with(
            "https://normalized.example"
        )

        session.close()


def test_navigate_rejects_invalid_url(tmp_path):
    executable = tmp_path / "chrome.exe"
    executable.write_text("fake")

    playwright = MagicMock()
    browser = MagicMock()
    page = MagicMock()

    playwright.chromium.launch.return_value = browser
    browser.new_page.return_value = page

    validator = InvalidUrlValidator()

    with patch(
        "brain.browser.interactive.playwright_browser_session.sync_playwright"
    ) as factory:

        factory.return_value.start.return_value = playwright

        session = PlaywrightBrowserSession(
            executable_path=str(executable),
            url_validator=validator,
        )

        session.start()

        with pytest.raises(
            ValueError,
            match="invalid URL",
        ):
            session.navigate("https://invalid.example")

        page.goto.assert_not_called()

        session.close()


def test_navigate_uses_url_validator(tmp_path):
    executable = tmp_path / "chrome.exe"
    executable.write_text("fake")

    playwright = MagicMock()
    browser = MagicMock()
    page = MagicMock()

    playwright.chromium.launch.return_value = browser
    browser.new_page.return_value = page

    validator = FakeUrlValidator()

    with patch(
        "brain.browser.interactive.playwright_browser_session.sync_playwright"
    ) as factory:

        factory.return_value.start.return_value = playwright

        session = PlaywrightBrowserSession(
            executable_path=str(executable),
            url_validator=validator,
        )

        session.start()
        session.navigate("anything")

        page.goto.assert_called_once_with(
            "https://normalized.example"
        )

        session.close()

def test_observation_requires_active_session(tmp_path):
    executable = tmp_path / "chrome.exe"
    executable.write_text("fake")

    session = PlaywrightBrowserSession(
        str(executable)
    )

    with pytest.raises(RuntimeError):
        session.observe()

def test_observe_returns_browser_observation(tmp_path):
    executable = tmp_path / "chrome.exe"
    executable.write_text("fake")

    playwright = MagicMock()
    browser = MagicMock()
    page = MagicMock()

    playwright.chromium.launch.return_value = browser
    browser.new_page.return_value = page

    page.url = "https://example.com"
    page.title.return_value = "Example"
    page.locator.return_value.inner_text.return_value = (
        "Example Domain"
    )

    with patch(
        "brain.browser.interactive.playwright_browser_session.sync_playwright"
    ) as factory:

        factory.return_value.start.return_value = playwright

        session = PlaywrightBrowserSession(
            str(executable)
        )

        session.start()

        observation = session.observe()

        assert observation.url == "https://example.com"
        assert observation.title == "Example"
        assert observation.text == "Example Domain"

        page.title.assert_called_once()
        page.locator.assert_called_once_with("body")
        page.locator.return_value.inner_text.assert_called_once()

        session.close()

def test_observe_does_not_navigate(tmp_path):
    executable = tmp_path / "chrome.exe"
    executable.write_text("fake")

    playwright = MagicMock()
    browser = MagicMock()
    page = MagicMock()

    playwright.chromium.launch.return_value = browser
    browser.new_page.return_value = page

    page.url = "https://example.com"
    page.title.return_value = "Example"
    page.locator.return_value.inner_text.return_value = (
        "Example Domain"
    )

    with patch(
        "brain.browser.interactive.playwright_browser_session.sync_playwright"
    ) as factory:

        factory.return_value.start.return_value = playwright

        session = PlaywrightBrowserSession(
            str(executable)
        )

        session.start()
        session.observe()

        page.goto.assert_not_called()

        session.close()

def test_observe_returns_browser_observation(tmp_path):
    executable = tmp_path / "chrome.exe"
    executable.write_text("fake")

    playwright = MagicMock()
    browser = MagicMock()
    page = MagicMock()

    playwright.chromium.launch.return_value = browser
    browser.new_page.return_value = page

    page.url = "https://example.com"
    page.title.return_value = "Example"

    element_locator = MagicMock()
    element_locator.count.return_value = 0

    body_locator = MagicMock()
    body_locator.inner_text.return_value = "Example page"

    def locator(selector):
        if selector == "body":
            return body_locator
        return element_locator

    page.locator.side_effect = locator

    with patch(
        "brain.browser.interactive.playwright_browser_session.sync_playwright"
    ) as factory:
        factory.return_value.start.return_value = playwright

        session = PlaywrightBrowserSession(str(executable))
        session.start()

        observation = session.observe()

        assert isinstance(observation, BrowserObservation)
        assert observation.url == "https://example.com"
        assert observation.title == "Example"
        assert observation.text == "Example page"
        assert observation.elements == frozenset()

        assert body_locator.inner_text.call_count == 1
        assert element_locator.count.call_count == 1

        session.close()