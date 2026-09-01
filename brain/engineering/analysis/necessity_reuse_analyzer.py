from abc import ABC
from abc import abstractmethod

from brain.engineering.analysis.models.analysis_request import (
    AnalysisRequest,
)

from brain.engineering.generation.models.engineering_decision import (
    EngineeringDecision,
)


class NecessityReuseAnalyzer(
    ABC,
):
    """
    Interface for determining implementation necessity
    and reuse opportunities.
    """

    @abstractmethod
    def analyze(
        self,
        request: AnalysisRequest,
    ) -> EngineeringDecision:
        """
        Analyze an engineering task for necessity and reuse.
        """
        pass