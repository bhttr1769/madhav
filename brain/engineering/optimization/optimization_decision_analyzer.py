from abc import ABC, abstractmethod

from brain.engineering.optimization.models.optimization_decision import (
    OptimizationDecision,
)
from brain.engineering.optimization.models.optimization_decision_request import (
    OptimizationDecisionRequest,
)


class OptimizationDecisionAnalyzer(ABC):
    """
    Defines the interface for determining whether and how a proposed
    implementation should be optimized.
    """

    @abstractmethod
    def analyze(
        self,
        request: OptimizationDecisionRequest,
    ) -> OptimizationDecision:
        """
        Analyze the engineering context and return a validated
        optimization decision.
        """
        raise NotImplementedError