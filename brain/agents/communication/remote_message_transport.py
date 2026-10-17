
from abc import ABC, abstractmethod


class RemoteMessageTransport(ABC):
    """Contract for transmitting authenticated messages to a remote endpoint."""

    @abstractmethod
    def send(self, endpoint: str, wire_bytes: bytes) -> None:
        """Transmit a signed message envelope to the specified endpoint."""
        raise NotImplementedError
