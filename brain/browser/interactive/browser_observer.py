from abc import ABC, abstractmethod

from brain.browser.interactive.models.browser_observation import (
    BrowserObservation,
)


class BrowserObserver(ABC):
    """
    Observes the current browser page.
    """

    @abstractmethod
    def observe(self) -> BrowserObservation:
        raise NotImplementedError