from abc import ABC, abstractmethod

from brain.engineering.generation.models.code_change import CodeChange


class ChangeApplier(ABC):
    @abstractmethod
    def apply(
        self,
        changes: tuple[CodeChange, ...],
    ) -> None:
        pass