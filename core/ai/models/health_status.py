from dataclasses import dataclass


@dataclass(frozen=True)
class HealthStatus:
    """
    Represents the health of the AI Runtime.
    """

    status: str

    provider: str

    provider_available: bool

    chat_model: str

    embedding_model: str

    chat_available: bool

    embedding_available: bool