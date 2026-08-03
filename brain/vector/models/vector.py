from dataclasses import dataclass


@dataclass(frozen=True)
class Vector:
    """
    Represents a numerical embedding vector.
    """

    values: list[float]

    @property
    def dimensions(self) -> int:
        """
        Returns the dimensionality of the vector.
        """
        return len(self.values)

    def __len__(self) -> int:
        return self.dimensions