from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime
from typing import Any
from brain.models.chunk import Chunk


@dataclass
class Document:
    """
    Universal knowledge object used throughout Madhav.
    """

    # ---------- Identity ----------

    name: str
    path: Path
    extension: str

    # ---------- Content ----------

    content: str

    # ---------- Metadata ----------

    size: int
    created_at: datetime
    modified_at: datetime

    # ---------- Knowledge ----------

    language: str = "unknown"
    source: str = "local"

    chunks: list[Chunk] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)