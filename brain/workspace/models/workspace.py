from dataclasses import dataclass

from brain.workspace.models.architecture import (
    Architecture,
)
from brain.workspace.models.dependency import (
    Dependency,
)
from brain.workspace.models.repository import (
    Repository,
)
from brain.workspace.models.technology import (
    Technology,
)


@dataclass(frozen=True)
class Workspace:
    """
    Complete workspace knowledge model.
    """

    repository: Repository

    technologies: set[Technology]

    dependencies: set[Dependency]

    architectures: set[Architecture]