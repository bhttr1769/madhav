from abc import ABC, abstractmethod

from brain.engineering.tasks.models.task_decomposition import (
    TaskDecomposition,
)

from brain.engineering.design.models.system_design import (
    SystemDesign,
)


class SystemDesigner(ABC):
    """
    Interface for designing a system from an engineering
    requirement and its task decomposition.
    """

    @abstractmethod
    def design(
        self,
        task_decomposition: TaskDecomposition,
    ) -> SystemDesign:
        """
        Produce a system design from the task decomposition.
        """
        pass