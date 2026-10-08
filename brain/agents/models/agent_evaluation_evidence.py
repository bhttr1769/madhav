from dataclasses import dataclass


_EXECUTION_STATUSES = frozenset(
    {
        "success",
        "failed",
    }
)

_VERIFICATION_STATUSES = frozenset(
    {
        "verified",
        "failed",
        "unknown",
    }
)

_OUTCOMES = frozenset(
    {
        "successful",
        "unsuccessful",
        "inconclusive",
    }
)


@dataclass(frozen=True)
class AgentEvaluationEvidence:
    """
    Normalized evidence describing the outcome of an agent's task work.

    This model does not calculate performance, reliability, or scores.
    It only represents evidence produced from existing execution and
    verification results.
    """

    agent_id: str
    task_id: str
    execution_status: str
    verification_status: str
    verification_passed: bool
    outcome: str

    def __post_init__(self) -> None:
        if not isinstance(self.agent_id, str):
            raise TypeError("agent_id must be a string")

        if not self.agent_id.strip():
            raise ValueError("agent_id must not be empty")

        if not isinstance(self.task_id, str):
            raise TypeError("task_id must be a string")

        if not self.task_id.strip():
            raise ValueError("task_id must not be empty")

        if not isinstance(self.execution_status, str):
            raise TypeError("execution_status must be a string")

        if self.execution_status not in _EXECUTION_STATUSES:
            raise ValueError(
                f"unsupported execution status: "
                f"{self.execution_status}"
            )

        if not isinstance(self.verification_status, str):
            raise TypeError("verification_status must be a string")

        if self.verification_status not in _VERIFICATION_STATUSES:
            raise ValueError(
                f"unsupported verification status: "
                f"{self.verification_status}"
            )

        if not isinstance(self.verification_passed, bool):
            raise TypeError(
                "verification_passed must be a bool"
            )

        if not isinstance(self.outcome, str):
            raise TypeError("outcome must be a string")

        if self.outcome not in _OUTCOMES:
            raise ValueError(
                f"unsupported evaluation outcome: "
                f"{self.outcome}"
            )

        if (
            self.verification_status == "verified"
            and not self.verification_passed
        ):
            raise ValueError(
                "verified status requires verification_passed=True"
            )

        if (
            self.verification_status in {"failed", "unknown"}
            and self.verification_passed
        ):
            raise ValueError(
                "failed or unknown verification status requires "
                "verification_passed=False"
            )

        if (
            self.verification_status == "verified"
            and self.outcome != "successful"
        ):
            raise ValueError(
                "verified evidence must have a successful outcome"
            )

        if (
            self.verification_status == "failed"
            and self.outcome != "unsuccessful"
        ):
            raise ValueError(
                "failed verification must have an unsuccessful outcome"
            )

        if (
            self.verification_status == "unknown"
            and self.outcome != "inconclusive"
        ):
            raise ValueError(
                "unknown verification must have an inconclusive outcome"
            )