from dataclasses import dataclass

from brain.engineering.requirements.models.requirement import (
    Requirement,
)

from brain.engineering.tasks.models.task import (
    Task,
)


@dataclass(frozen=True)
class TaskDecomposition:
    """
    Represents an ordered decomposition of an engineering requirement.
    """

    requirement: Requirement

    tasks: tuple[Task, ...]