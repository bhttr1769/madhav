from brain.browser.interactive.browser_session import BrowserSession
from brain.browser.interactive.models.browser_session_state import (
    BrowserSessionState,
)


class FakeBrowserSession(BrowserSession):

    def __init__(self):
        self.started = False
        self.url = None

    def start(self):
        self.started = True

    def close(self):
        self.started = False
        self.url = None

    def observe(self):
        raise NotImplementedError

    def navigate(self, url):
        self.url = url

    def current_state(self):
        return BrowserSessionState(
            active=self.started,
            url=self.url,
        )


def test_browser_session_contract_supports_lifecycle_and_state():
    session = FakeBrowserSession()

    assert session.current_state() == BrowserSessionState(
        active=False,
        url=None,
    )

    session.start()

    assert session.current_state() == BrowserSessionState(
        active=True,
        url=None,
    )

    session.navigate("https://example.com")

    assert session.current_state() == BrowserSessionState(
        active=True,
        url="https://example.com",
    )

    session.close()

    assert session.current_state() == BrowserSessionState(
        active=False,
        url=None,
    )