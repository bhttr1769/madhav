from dataclasses import dataclass


@dataclass(frozen=True)
class CapabilityExecutionRequest:
    capability_id: str
    input_data: object