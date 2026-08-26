from dataclasses import dataclass


@dataclass(frozen=True)
class CallModel:
    """
    Represents a function or method call in Python code.
    """

    caller: str

    callee: str

    module: str