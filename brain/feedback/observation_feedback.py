from brain.feedback.feedback_evaluator import (
    FeedbackEvaluator,
)

from brain.feedback.models.expected_outcome import (
    ExpectedOutcome,
)

from brain.feedback.models.feedback_result import (
    FeedbackResult,
)

from brain.feedback.models.observation_transition import (
    ObservationTransition,
)

from brain.perception.models.observation import (
    Observation,
)


class ObservationFeedback:
    """
    Evaluates an expected post-action state against
    observations captured before and after an action.

    This component does not execute actions and does not
    produce observations itself.
    """

    def __init__(
        self,
        evaluator: FeedbackEvaluator | None = None,
    ):
        self._evaluator = (
            evaluator
            if evaluator is not None
            else FeedbackEvaluator()
        )

    def evaluate(
        self,
        before: frozenset[Observation],
        after: frozenset[Observation],
        expected: ExpectedOutcome,
    ) -> FeedbackResult:

        transition = ObservationTransition(
            before=before,
            after=after,
        )

        return self._evaluator.evaluate(
            expected,
            transition.after,
        )