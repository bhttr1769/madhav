from dataclasses import dataclass

from brain.browser.interactive.models.browser_element import BrowserElement
from brain.safety.models.action import Action


@dataclass(frozen=True)
class BrowserAction:
    """
    Represents an intended interaction with the browser.
    """

    action_type: str
    target: BrowserElement | None = None
    text: str | None = None
    key: str | None = None
    url: str | None = None

    def to_action(self) -> Action:
        target = self.url

        if target is None and self.target is not None:
            target = self.target.selector

        return Action(
            name=self.action_type,
            category="browser",
            target=target,
        )