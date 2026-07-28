from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime
from typing import Any


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

    # ---------- Future ----------

    chunks: list[str] = field(default_factory=list)
    embedding: list[float] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)