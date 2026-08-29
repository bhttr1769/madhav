from abc import ABC, abstractmethod

from brain.engineering.requirements.models.requirement import (
    Requirement,
)

from brain.engineering.tasks.models.task_decomposition import (
    TaskDecomposition,
)


class TaskDecomposer(ABC):
    """
    Interface for decomposing engineering requirements into tasks.
    """

    @abstractmethod
    def decompose(
        self,
        requirement: Requirement,
    ) -> TaskDecomposition:
        """
        Decompose a structured requirement into ordered tasks.
        """
        pass