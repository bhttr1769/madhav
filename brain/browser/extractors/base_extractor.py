from abc import ABC
from abc import abstractmethod


class BaseExtractor(
    ABC,
):
    """
    Base content extractor.
    """

    @abstractmethod
    def can_extract(
        self,
        document,
    ) -> bool:

        pass

    @abstractmethod
    def extract(
        self,
        document,
    ):

        pass