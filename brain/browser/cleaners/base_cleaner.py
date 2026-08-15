from abc import ABC
from abc import abstractmethod


class BaseCleaner(
    ABC,
):
    """
    Base content cleaner.
    """

    @abstractmethod
    def can_clean(
        self,
        extracted_content,
    ) -> bool:

        pass

    @abstractmethod
    def clean(
        self,
        extracted_content,
    ):

        pass