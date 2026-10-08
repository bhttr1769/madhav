from dataclasses import dataclass


@dataclass(frozen=True)
class AgentPerformanceRecord:
    """
    Aggregate performance information for one agent.

    This record contains observed evaluation counts. It does not
    execute work, perform verification, or assign an agent.
    """

    agent_id: str
    total_evaluations: int = 0
    successful_outcomes: int = 0
    unsuccessful_outcomes: int = 0
    inconclusive_outcomes: int = 0
    verified_successes: int = 0
    verified_failures: int = 0

    def __post_init__(self) -> None:
        if not isinstance(self.agent_id, str):
            raise TypeError("agent_id must be a string")

        if not self.agent_id.strip():
            raise ValueError("agent_id must not be empty")

        fields = (
            ("total_evaluations", self.total_evaluations),
            ("successful_outcomes", self.successful_outcomes),
            ("unsuccessful_outcomes", self.unsuccessful_outcomes),
            ("inconclusive_outcomes", self.inconclusive_outcomes),
            ("verified_successes", self.verified_successes),
            ("verified_failures", self.verified_failures),
        )

        for field_name, value in fields:
            if isinstance(value, bool) or not isinstance(value, int):
                raise TypeError(
                    f"{field_name} must be an integer"
                )

            if value < 0:
                raise ValueError(
                    f"{field_name} must not be negative"
                )

        outcome_total = (
            self.successful_outcomes
            + self.unsuccessful_outcomes
            + self.inconclusive_outcomes
        )

        if outcome_total != self.total_evaluations:
            raise ValueError(
                "outcome counts must equal total_evaluations"
            )

        verified_total = (
            self.verified_successes
            + self.verified_failures
        )

        if verified_total > self.total_evaluations:
            raise ValueError(
                "verified counts cannot exceed total_evaluations"
            )

    @property
    def reliability(self) -> float:
        """
        Reliability based only on evaluations with known verification.
        """
        verified_total = (
            self.verified_successes
            + self.verified_failures
        )

        if verified_total == 0:
            return 0.0

        return self.verified_successes / verified_total