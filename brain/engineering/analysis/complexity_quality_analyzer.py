from abc import ABC, abstractmethod

from brain.engineering.analysis.models.complexity_quality_request import (
    ComplexityQualityRequest,
)

from brain.engineering.analysis.models.engineering_quality_assessment import (
    EngineeringQualityAssessment,
)


class ComplexityQualityAnalyzer(
    ABC,
):
    """
    Defines the interface for complexity and implementation-quality analysis.
    """

    @abstractmethod
    def analyze(
        self,
        request: ComplexityQualityRequest,
    ) -> EngineeringQualityAssessment:
        """
        Analyze a proposed implementation and return a validated
        engineering-quality assessment.
        """
        raise NotImplementedError