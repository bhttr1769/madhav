from dataclasses import dataclass

from brain.capabilities.models.capability_descriptor import (
    CapabilityDescriptor,
)
from brain.capabilities.models.capability_assessment import (
    CapabilityAssessment,
)
from brain.evolution.models.evolution_experience import (
    EvolutionExperience,
)
from brain.evolution.models.evolution_request import (
    EvolutionRequest,
)


@dataclass(frozen=True)
class EvolutionPlanningContext:
    request: EvolutionRequest
    assessment: CapabilityAssessment
    available_capabilities: tuple[
        CapabilityDescriptor,
        ...,
    ]
    experiences: tuple[
        EvolutionExperience,
        ...,
    ] = ()