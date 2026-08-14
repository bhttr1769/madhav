from abc import ABC
from abc import abstractmethod


class BaseDetector(ABC):
    """
    Base interface for all workspace detectors.
    """

    @abstractmethod
    def detect(
        self,
        signatures,
    ):

        pass