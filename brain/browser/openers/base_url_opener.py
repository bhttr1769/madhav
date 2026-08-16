from abc import ABC
from abc import abstractmethod


class BaseUrlOpener(
    ABC,
):
    """
    Opens URLs and returns their content.
    """

    @abstractmethod
    def open(
        self,
        url: str,
    ):

        pass