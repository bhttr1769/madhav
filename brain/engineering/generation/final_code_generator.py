from abc import ABC, abstractmethod

from brain.engineering.generation.models.final_generation_request import (
    FinalGenerationRequest,
)
from brain.engineering.generation.models.generation_result import (
    GenerationResult,
)


class FinalCodeGenerator(ABC):
    """
    Defines the interface for generating the final implementation
    after engineering analysis and optimization decisions.
    """

    @abstractmethod
    def generate(
        self,
        request: FinalGenerationRequest,
    ) -> GenerationResult:
        """
        Generate the final implementation from the complete
        engineering context.
        """
        raise NotImplementedError