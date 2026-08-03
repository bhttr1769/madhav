from dataclasses import dataclass, field
from typing import Any


@dataclass
class Chunk:
    """
    Represents a single chunk of a document.
    """

    # ---------- Identity ----------

    id: int

    # ---------- Content ----------

    text: str

    # ---------- Location ----------

    start_char: int
    end_char: int

    # ---------- Statistics ----------

    token_count: int

    # ---------- AI ----------

    embedding: list[float] | None = None

    # ---------- Metadata ----------

    metadata: dict[str, Any] = field(default_factory=dict)