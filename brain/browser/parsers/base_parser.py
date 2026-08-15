from abc import ABC
from abc import abstractmethod


class BaseParser(
    ABC,
):
    """
    Base document parser.
    """

    @abstractmethod
    def can_parse(
        self,
        content: str,
    ) -> bool:

        pass

    @abstractmethod
    def parse(
        self,
        content: str,
    ):

        pass