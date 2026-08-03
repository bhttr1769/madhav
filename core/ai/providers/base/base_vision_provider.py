from abc import abstractmethod

from core.ai.providers.base.base_provider import BaseProvider


class BaseVisionProvider(BaseProvider):
    """
    Interface for providers that support vision.
    """

    @abstractmethod
    def analyze_image(self, image: bytes) -> str:
        """
        Analyze an image and return a textual description.
        """
        pass