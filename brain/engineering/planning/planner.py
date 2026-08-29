from abc import ABC, abstractmethod

from brain.engineering.tasks.models.task_decomposition import (
    TaskDecomposition,
)

from brain.engineering.planning.models.plan import (
    EngineeringPlan,
)


class Planner(ABC):
    """
    Interface for engineering planning.
    """

    @abstractmethod
    def plan(
        self,
        decomposition: TaskDecomposition,
    ) -> EngineeringPlan:
        """
        Create an engineering plan from a task decomposition.
        """
        pass