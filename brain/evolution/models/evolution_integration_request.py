from dataclasses import dataclass

from brain.capabilities.models.capability_descriptor_request import (
    CapabilityDescriptorRequest,
)


@dataclass(frozen=True)
class EvolutionIntegrationRequest:
    capability: CapabilityDescriptorRequest