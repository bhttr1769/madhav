from brain.feedback.models.expected_outcome import (
    ExpectedOutcome,
)

from brain.feedback.models.feedback_result import (
    FeedbackResult,
)

from brain.perception.models.observation import (
    Observation,
)


class FeedbackEvaluator:
    """
    Compares an expected outcome with observed state.

    Verification is established only when every expected
    observation is present in the observed state.

    Missing expected observations result in UNKNOWN,
    because absence of an observation does not prove
    that the expected state failed to occur.
    """

    VERIFIED = "verified"
    UNKNOWN = "unknown"

    def evaluate(
        self,
        expected: ExpectedOutcome,
        observed: frozenset[Observation],
    ) -> FeedbackResult:

        if not isinstance(
            expected,
            ExpectedOutcome,
        ):
            raise TypeError(
                "expected must be an ExpectedOutcome"
            )

        if not isinstance(
            observed,
            frozenset,
        ):
            raise TypeError(
                "observed must be a frozenset"
            )

        for observation in observed:
            if not isinstance(
                observation,
                Observation,
            ):
                raise TypeError(
                    "observed must contain only "
                    "Observation instances"
                )

        if expected.observations.issubset(
            observed
        ):
            status = self.VERIFIED
        else:
            status = self.UNKNOWN

        return FeedbackResult(
            status=status,
            expected=expected.observations,
            observed=observed,
        )