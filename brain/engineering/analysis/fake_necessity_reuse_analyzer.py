from brain.engineering.generation.models.engineering_decision import (
    EngineeringDecision,
)
from brain.engineering.analysis.necessity_reuse_analyzer import (
    NecessityReuseAnalyzer,
)


class FakeNecessityReuseAnalyzer(NecessityReuseAnalyzer):
    """
    Deterministic analyzer for tests and dependency injection.
    """

    def __init__(
        self,
        result: EngineeringDecision,
    ):
        self._result = result

    def analyze(
        self,
        task,
        design,
        code_structure,
    ) -> EngineeringDecision:

        return self._result
