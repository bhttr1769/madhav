from dataclasses import dataclass


_FAILURE_CATEGORIES = frozenset(
    {
        "execution",
        "validation",
        "dependency",
        "timeout",
        "unknown",
    }
)


@dataclass(frozen=True)
class CapabilityFailure:
    capability_id: str
    category: str
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

        if not isinstance(self.category, str):
            raise TypeError(
                "category must be a string"
            )

        if self.category not in _FAILURE_CATEGORIES:
            raise ValueError(
                f"unsupported failure category: {self.category}"
            )

        if not isinstance(self.rationale, str):
            raise TypeError(
                "rationale must be a string"
            )

        if not self.rationale.strip():
            raise ValueError(
                "rationale must not be empty"
            )