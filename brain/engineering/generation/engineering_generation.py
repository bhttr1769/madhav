from abc import ABC, abstractmethod

from brain.engineering.generation.models.engineering_generation_request import (
    EngineeringGenerationRequest,
)
from brain.engineering.generation.models.engineering_generation_result import (
    EngineeringGenerationResult,
)


class EngineeringGeneration(ABC):
    """
    Defines the interface for integrated engineering analysis,
    optimization, and code generation.
    """

    @abstractmethod
    def generate(
        self,
        request: EngineeringGenerationRequest,
    ) -> EngineeringGenerationResult:
        """
        Execute the complete engineering generation workflow.
        """
        raise NotImplementedError