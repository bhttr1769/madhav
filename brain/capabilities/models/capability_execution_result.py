from dataclasses import dataclass


_EXECUTION_STATUSES = frozenset(
    {
        "success",
        "failed",
    }
)


@dataclass(frozen=True)
class CapabilityExecutionResult:
    capability_id: str
    output: object
    status: str = "success"
    error: object = None

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

        if self.status not in _EXECUTION_STATUSES:
            raise ValueError(
                f"unsupported execution status: {self.status}"
            )

        if self.status == "success" and self.error is not None:
            raise ValueError(
                "successful execution cannot contain an error"
            )

        if self.status == "failed" and self.error is None:
            raise ValueError(
                "failed execution must contain an error"
            )