from abc import ABC, abstractmethod

from brain.engineering.generation.models.generation_request import (
    GenerationRequest,
)

from brain.engineering.generation.models.generation_result import (
    GenerationResult,
)


class CodeGenerator(ABC):
    """
    Interface for generating code changes.
    """

    @abstractmethod
    def generate(
        self,
        request: GenerationRequest,
    ) -> GenerationResult:
        """
        Generate code changes from an engineering generation request.
        """
        pass