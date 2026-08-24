from dataclasses import dataclass
from typing import Any

from brain.knowledge.models.node_type import (
    NodeType,
)


@dataclass(
    frozen=True,
)
class Node:
    """
    Represents an entity in the knowledge graph.
    """

    id: str

    type: NodeType

    name: str

    properties: dict[str, Any]

    metadata: dict[str, Any]