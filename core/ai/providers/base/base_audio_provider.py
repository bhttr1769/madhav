from abc import abstractmethod

from core.ai.providers.base.base_provider import BaseProvider


class BaseAudioProvider(BaseProvider):
    """
    Interface for providers that support audio.
    """

    @abstractmethod
    def transcribe(self, audio: bytes) -> str:
        """
        Convert speech to text.
        """
        pass