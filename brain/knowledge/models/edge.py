from dataclasses import dataclass
from typing import Any

from brain.knowledge.models.edge_type import (
    EdgeType,
)


@dataclass(
    frozen=True,
)
class Edge:
    """
    Represents a directed relationship between
    two nodes in the knowledge graph.
    """

    id: str

    source_id: str

    target_id: str

    type: EdgeType

    properties: dict[str, Any]

    metadata: dict[str, Any]