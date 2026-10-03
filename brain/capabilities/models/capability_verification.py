from dataclasses import dataclass


_VERIFICATION_STATUSES = frozenset(
    {
        "verified",
        "failed",
        "unknown",
    }
)


@dataclass(frozen=True)
class CapabilityVerification:
    capability_id: str
    passed: bool
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

        if not isinstance(self.passed, bool):
            raise TypeError(
                "passed must be a bool"
            )

        if not isinstance(self.status, str):
            raise TypeError(
                "status must be a string"
            )

        if self.status not in _VERIFICATION_STATUSES:
            raise ValueError(
                f"unsupported verification status: "
                f"{self.status}"
            )

        if not isinstance(self.rationale, str):
            raise TypeError(
                "rationale must be a string"
            )

        if not self.rationale.strip():
            raise ValueError(
                "rationale must not be empty"
            )

        if self.status == "verified" and not self.passed:
            raise ValueError(
                "verified status requires passed=True"
            )

        if self.status == "failed" and self.passed:
            raise ValueError(
                "failed status requires passed=False"
            )

        if self.status == "unknown" and self.passed:
            raise ValueError(
                "unknown status requires passed=False"
            )