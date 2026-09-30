from dataclasses import dataclass


@dataclass(frozen=True)
class CapabilityAssessment:
    requested_capability: str | frozenset[str]
    available: bool
    status: str
    matched_capabilities: frozenset[str]
    missing_capabilities: frozenset[str]
    rationale: str