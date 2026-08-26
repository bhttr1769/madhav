from abc import ABC, abstractmethod

from brain.reasoning.models.context import (
    Context,
)


class Reasoner(ABC):
    """
    Produces reasoning results from contextual information.
    """

    @abstractmethod
    def reason(
        self,
        context: Context,
    ):
        """
        Reason over the supplied context.
        """
        raise NotImplementedError