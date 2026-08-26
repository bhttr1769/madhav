from dataclasses import dataclass


@dataclass(frozen=True)
class Screen:
    """
    Represents a captured screen.
    """

    width: int

    height: int

    image_path: str | None = None

    metadata: frozenset[
        tuple[str, str]
    ] = frozenset()