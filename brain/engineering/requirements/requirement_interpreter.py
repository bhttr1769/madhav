from abc import ABC, abstractmethod

from brain.engineering.requirements.models.requirement import (
    Requirement,
)


class RequirementInterpreter(ABC):
    """
    Interface for interpreting engineering requests.
    """

    @abstractmethod
    def interpret(
        self,
        request: str,
    ) -> Requirement:
        raise NotImplementedError