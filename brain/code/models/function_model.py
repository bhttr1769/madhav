from dataclasses import dataclass


@dataclass(frozen=True)
class FunctionModel:
    """
    Represents a Python function or method.
    """

    name: str

    module: str

    class_name: str | None

    parameters: frozenset[str]

    is_async: bool