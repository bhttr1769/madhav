from dataclasses import dataclass


@dataclass(frozen=True)
class ModelConfig:
    """
    Configuration for a specific AI model.
    """

    name: str
    temperature: float = 0.7
    max_tokens: int | None = None