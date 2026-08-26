from dataclasses import dataclass

from brain.workspace.models.directory import (
    Directory,
)

from brain.workspace.models.file import (
    File,
)

from brain.workspace.models.signature import (
    Signature,
)


@dataclass(frozen=True)
class ParsedRepository:
    """
    Represents structured repository parsing results.
    """

    root: str

    files: frozenset[File]

    directories: frozenset[Directory]

    signatures: frozenset[Signature]