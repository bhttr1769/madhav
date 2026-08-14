from dataclasses import dataclass

from brain.workspace.models.signature import (
    Signature,
)


@dataclass(frozen=True)
class Repository:
    """
    Represents a workspace repository.
    """

    files: int

    directories: int

    signatures: set[Signature]