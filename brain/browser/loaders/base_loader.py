from abc import ABC
from abc import abstractmethod


class BaseLoader(
    ABC,
):
    """
    Base document loader.
    """

    @abstractmethod
    def can_load(
        self,
        response,
    ) -> bool:

        pass

    @abstractmethod
    def load(
        self,
        response,
    ):

        pass