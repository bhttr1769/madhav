from dataclasses import dataclass, field
from typing import Any


@dataclass
class Edge:
    """
    Represents a relationship between two knowledge entities.
    """

    # ---------- Identity ----------

    id: str

    # ---------- Relationship ----------

    source: str

    target: str

    relation: str

    # ---------- Metadata ----------

    metadata: dict[str, Any] = field(
        default_factory=dict
    )