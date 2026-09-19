from dataclasses import dataclass

from brain.capabilities.models.capability_descriptor import (
    CapabilityDescriptor,
)


@dataclass(frozen=True)
class CapabilityComposition:
    id: str
    name: str
    description: str
    version: str
    capabilities: tuple[CapabilityDescriptor, ...]