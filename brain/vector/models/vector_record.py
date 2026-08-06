from dataclasses import dataclass, field

from brain.vector.models.vector import Vector


@dataclass
class VectorRecord:
    """
    Represents a stored vector and its associated metadata.
    """

    id: str

    vector: Vector

    document_id: str

    chunk_id: int

    text: str

    metadata: dict[str, str] = field(default_factory=dict)