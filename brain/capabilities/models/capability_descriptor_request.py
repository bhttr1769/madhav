from dataclasses import dataclass


@dataclass(frozen=True)
class CapabilityDescriptorRequest:
    id: str
    name: str
    description: str
    version: str
    entry_point: str
    dependencies: frozenset[str]