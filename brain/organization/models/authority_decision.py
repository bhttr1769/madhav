from dataclasses import dataclass


@dataclass(frozen=True)
class AuthorityDecision:
    """The result of evaluating organizational authority."""

    allowed: bool
    reason: str
    delegation_id: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.allowed, bool):
            raise TypeError("allowed must be a boolean")

        if not isinstance(self.reason, str):
            raise TypeError("reason must be a string")

        if not self.reason.strip():
            raise ValueError("reason must not be empty")

        if self.delegation_id is not None:
            if not isinstance(self.delegation_id, str):
                raise TypeError("delegation_id must be a string or None")

            if not self.delegation_id.strip():
                raise ValueError("delegation_id must not be empty")