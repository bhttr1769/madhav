from dataclasses import dataclass


@dataclass(frozen=True)
class CapabilityDescriptor:
    id: str
    name: str
    description: str
    version: str
    entry_point: str
    dependencies: frozenset[str]
    input_contract: str = "object"
    output_contract: str = "object"