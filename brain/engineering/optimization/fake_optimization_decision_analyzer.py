from brain.engineering.optimization.models.optimization_decision import (
    OptimizationDecision,
)
from brain.engineering.optimization.models.optimization_decision_request import (
    OptimizationDecisionRequest,
)
from brain.engineering.optimization.optimization_decision_analyzer import (
    OptimizationDecisionAnalyzer,
)


class FakeOptimizationDecisionAnalyzer(
    OptimizationDecisionAnalyzer,
):
    """
    Deterministic optimization-decision analyzer intended for tests
    and local engineering workflows.
    """

    def __init__(
        self,
        decision: OptimizationDecision,
    ):
        if not isinstance(
            decision,
            OptimizationDecision,
        ):
            raise TypeError(
                "decision must be an OptimizationDecision"
            )

        self._decision = decision
        self.last_request = None

    def analyze(
        self,
        request: OptimizationDecisionRequest,
    ) -> OptimizationDecision:
        if not isinstance(
            request,
            OptimizationDecisionRequest,
        ):
            raise TypeError(
                "request must be an OptimizationDecisionRequest"
            )

        self.last_request = request

        return self._decision