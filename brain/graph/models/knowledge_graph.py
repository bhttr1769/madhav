from dataclasses import dataclass, field

from brain.graph.models.node import Node
from brain.graph.models.edge import Edge


@dataclass
class KnowledgeGraph:
    """
    Represents the complete knowledge graph.
    """

    nodes: dict[str, Node] = field(
        default_factory=dict
    )

    edges: dict[str, Edge] = field(
        default_factory=dict
    )