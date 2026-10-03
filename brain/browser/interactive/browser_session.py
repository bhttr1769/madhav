from abc import abstractmethod

from brain.browser.interactive.browser_observer import BrowserObserver
from brain.browser.interactive.models.browser_observation import BrowserObservation
from brain.browser.interactive.models.browser_session_state import BrowserSessionState


class BrowserSession(BrowserObserver):
    @abstractmethod
    def start(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def navigate(self, url: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def current_state(self) -> BrowserSessionState:
        raise NotImplementedError

    @abstractmethod
    def observe(self) -> BrowserObservation:
        raise NotImplementedError