from brain.browser.interactive.browser_executor import BrowserExecutor
from brain.browser.interactive.browser_session import BrowserSession
from brain.browser.interactive.models.browser_action import BrowserAction


class PlaywrightBrowserExecutor(BrowserExecutor):
    def __init__(self, session: BrowserSession):
        if not isinstance(session, BrowserSession):
            raise TypeError(
                "session must be a BrowserSession"
            )

        self._session = session

    def execute(self, action: BrowserAction) -> None:
        if not isinstance(action, BrowserAction):
            raise TypeError(
                "action must be a BrowserAction"
            )

        page = self._session._page

        if page is None:
            raise RuntimeError(
                "browser session is not active"
            )

        if action.action_type == "navigate":
            if not action.url:
                raise ValueError(
                    "navigate action requires a url"
                )

            self._session.navigate(action.url)
            return

        if action.target is None:
            raise ValueError(
                f"{action.action_type} action requires a target"
            )

        locator = page.locator(action.target.selector)

        if action.action_type == "click":
            locator.click()
            return

        if action.action_type == "type":
            if action.text is None:
                raise ValueError(
                    "type action requires text"
                )

            locator.fill(action.text)
            return

        if action.action_type == "press":
            if action.key is None:
                raise ValueError(
                    "press action requires key"
                )

            locator.press(action.key)
            return

        raise ValueError(
            f"unsupported browser action: {action.action_type}"
        )