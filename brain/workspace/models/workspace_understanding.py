from dataclasses import dataclass


@dataclass(frozen=True)
class WorkspaceUnderstanding:
    """
    Represents synthesized understanding of a workspace.
    """

    name: str

    root: str

    files: int

    directories: int

    technologies: frozenset[str]

    dependencies: frozenset[str]

    architectures: frozenset[str]