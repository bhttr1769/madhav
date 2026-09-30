from abc import ABC, abstractmethod

from brain.ui.models.ui_action import UIAction


class UIActionExecutor(ABC):
    """
    Executes validated desktop UI actions.
    """

    @abstractmethod
    def execute(
        self,
        action: UIAction,
    ) -> None:
        """
        Execute a UI action.
        """
        raise NotImplementedError