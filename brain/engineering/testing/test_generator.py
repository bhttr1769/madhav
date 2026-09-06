from abc import ABC, abstractmethod

from brain.engineering.testing.models.test_generation_request import (
    TestGenerationRequest,
)

from brain.engineering.testing.models.test_generation_result import (
    TestGenerationResult,
)


class TestGenerator(ABC):
    """
    Interface for generating tests for an implementation.
    """

    @abstractmethod
    def generate(
        self,
        request: TestGenerationRequest,
    ) -> TestGenerationResult:
        """
        Generate test changes from a test generation request.
        """
        pass