from dataclasses import dataclass

from brain.agents.context_source_status import ContextSourceStatus


@dataclass(frozen=True)
class ContextSourceResult:
    source: object
    status: ContextSourceStatus
    value: object | None = None
    error: object | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.status, ContextSourceStatus):
            raise TypeError(
                "status must be a ContextSourceStatus"
            )

        if self.status == ContextSourceStatus.AVAILABLE:
            if self.value is None:
                raise ValueError(
                    "available source result must contain a value"
                )
            if self.error is not None:
                raise ValueError(
                    "available source result cannot contain an error"
                )

        if self.status == ContextSourceStatus.FAILED:
            if self.error is None:
                raise ValueError(
                    "failed source result must contain an error"
                )