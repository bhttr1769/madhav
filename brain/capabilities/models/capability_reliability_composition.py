from dataclasses import dataclass

from brain.capabilities.models.capability_composition import (
    CapabilityComposition,
)
from brain.capabilities.models.capability_reliability_assessment import (
    CapabilityReliabilityAssessment,
)


@dataclass(frozen=True)
class CapabilityReliabilityComposition:
    composition: CapabilityComposition
    assessments: tuple[CapabilityReliabilityAssessment, ...]