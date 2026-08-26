from abc import ABC, abstractmethod

from brain.ui.models.screen import (
    Screen,
)


class ScreenCapture(ABC):
    """
    Captures the current screen.
    """

    @abstractmethod
    def capture(self) -> Screen:
        """
        Capture the current screen.
        """
        raise NotImplementedError