from dataclasses import dataclass


@dataclass(frozen=True)
class ParsedModule:
    """
    Represents the result of parsing a Python source file.
    """

    path: str

    source: str

    node_count: int