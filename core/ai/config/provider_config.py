from dataclasses import dataclass


@dataclass(frozen=True)
class ProviderConfig:
    """
    Configuration for an AI provider.
    """

    name: str
    endpoint: str
    timeout: int = 60