from dataclasses import dataclass


_RELIABILITY_STATUSES = frozenset(
    {
        "reliable",
        "unreliable",
        "unknown",
    }
)


@dataclass(frozen=True)
class CapabilityReliabilityAssessment:
    capability_id: str
    status: str
    evidence: object
    rationale: str

    def __post_init__(self):
        if not isinstance(self.capability_id, str):
            raise TypeError(
                "capability_id must be a string"
            )

        if not self.capability_id.strip():
            raise ValueError(
                "capability_id must not be empty"
            )

        if not isinstance(self.status, str):
            raise TypeError(
                "status must be a string"
            )

        if self.status not in _RELIABILITY_STATUSES:
            raise ValueError(
                f"unsupported reliability status: {self.status}"
            )

        if not isinstance(self.rationale, str):
            raise TypeError(
                "rationale must be a string"
            )

        if not self.rationale.strip():
            raise ValueError(
                "rationale must not be empty"
            )