from abc import ABC, abstractmethod

from brain.browser.interactive.models.browser_action import BrowserAction


class BrowserExecutor(ABC):
    @abstractmethod
    def execute(self, action: BrowserAction) -> None:
        raise NotImplementedError