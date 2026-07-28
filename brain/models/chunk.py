from dataclasses import dataclass, field
from typing import Any


@dataclass
class Chunk:
    """
    Represents the smallest unit of knowledge in Madhav.
    """

    id: int
    text: str

    start_char: int
    end_char: int

    token_count: int = 0

    embedding: list[float] | None = None

    metadata: dict[str, Any] = field(default_factory=dict)