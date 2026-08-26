from abc import ABC, abstractmethod

from brain.ui.models.screen import (
    Screen,
)

from brain.ui.models.ui_element import (
    UIElement,
)


class UIElementDetector(ABC):
    """
    Detects user-interface elements from a screen.
    """

    @abstractmethod
    def detect(
        self,
        screen: Screen,
    ) -> frozenset[UIElement]:
        """
        Detect UI elements from a screen.
        """
        raise NotImplementedError