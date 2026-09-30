from dataclasses import dataclass


@dataclass(frozen=True)
class CapabilityExecutionResult:
    capability_id: str
    output: object