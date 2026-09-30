from collections.abc import Callable

from brain.feedback.models.expected_outcome import (
    ExpectedOutcome,
)

from brain.feedback.models.feedback_result import (
    FeedbackResult,
)

from brain.feedback.observation_feedback import (
    ObservationFeedback,
)

from brain.perception.models.observation import (
    Observation,
)


class ActionObservationOrchestrator:
    """
    Coordinates observation, action execution, post-action
    observation, and feedback evaluation.

    This component does not:
    - execute actions itself
    - perform safety checks
    - produce observations
    - evaluate feedback directly
    """

    def __init__(
        self,
        observe: Callable[[], frozenset[Observation]],
        execute: Callable[[object], object],
        feedback: ObservationFeedback | None = None,
    ):
        if not callable(observe):
            raise TypeError(
                "observe must be callable"
            )

        if not callable(execute):
            raise TypeError(
                "execute must be callable"
            )

        if feedback is not None and not isinstance(
            feedback,
            ObservationFeedback,
        ):
            raise TypeError(
                "feedback must be an ObservationFeedback"
            )

        self._observe = observe
        self._execute = execute
        self._feedback = (
            feedback
            if feedback is not None
            else ObservationFeedback()
        )

    def execute(
        self,
        action: object,
        expected: ExpectedOutcome,
    ) -> tuple[object, FeedbackResult]:

        if not isinstance(
            expected,
            ExpectedOutcome,
        ):
            raise TypeError(
                "expected must be an ExpectedOutcome"
            )

        before = self._observe()

        if not isinstance(
            before,
            frozenset,
        ):
            raise TypeError(
                "observe must return a frozenset"
            )

        for observation in before:
            if not isinstance(
                observation,
                Observation,
            ):
                raise TypeError(
                    "observe must return a frozenset "
                    "containing only Observation instances"
                )

        execution_result = self._execute(
            action,
        )

        after = self._observe()

        if not isinstance(
            after,
            frozenset,
        ):
            raise TypeError(
                "observe must return a frozenset"
            )

        for observation in after:
            if not isinstance(
                observation,
                Observation,
            ):
                raise TypeError(
                    "observe must return a frozenset "
                    "containing only Observation instances"
                )

        feedback_result = self._feedback.evaluate(
            before=before,
            after=after,
            expected=expected,
        )

        return (
            execution_result,
            feedback_result,
        )