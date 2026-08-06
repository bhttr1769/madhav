from dataclasses import dataclass, field
from typing import Any


@dataclass
class Node:
    """
    Represents a knowledge entity in the graph.
    """

    # ---------- Identity ----------

    id: str

    # ---------- Entity ----------

    name: str

    type: str

    # ---------- Metadata ----------

    metadata: dict[str, Any] = field(
        default_factory=dict
    )