from dataclasses import dataclass


@dataclass(frozen=True)
class ImportModel:
    """
    Represents a Python import statement.
    """

    module: str

    name: str | None

    alias: str | None

    level: int = 0