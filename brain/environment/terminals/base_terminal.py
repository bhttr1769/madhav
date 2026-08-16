from abc import ABC
from abc import abstractmethod


class BaseTerminal(
    ABC,
):
    """
    Terminal abstraction.
    """

    @abstractmethod
    def execute(
        self,
        command,
    ):

        pass