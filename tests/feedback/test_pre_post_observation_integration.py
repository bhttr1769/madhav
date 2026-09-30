import pytest

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

from brain.feedback.observation_feedback import (
    ObservationFeedback,
)

from brain.perception.models.observation import (
    Observation,
)


def _observation(
    source: str,
    category: str,
    subject: str,
    value: str,
) -> Observation:

    return Observation(
        source=source,
        category=category,
        subject=subject,
        value=value,
    )


def test_observation_transition_preserves_before_and_after():

    before = frozenset({
        _observation(
            "environment",
            "file",
            "project",
            "old_state",
        ),
    })

    after = frozenset({
        _observation(
            "environment",
            "file",
            "project",
            "new_state",
        ),
    })

    transition = ObservationTransition(
        before=before,
        after=after,
    )

    assert transition.before == before
    assert transition.after == after


def test_observation_transition_is_immutable():

    transition = ObservationTransition(
        before=frozenset(),
        after=frozenset(),
    )

    with pytest.raises(AttributeError):
        transition.before = frozenset()


def test_observation_transition_rejects_non_frozenset_before():

    with pytest.raises(
        TypeError,
        match="before must be a frozenset",
    ):
        ObservationTransition(
            before=set(),
            after=frozenset(),
        )


def test_observation_transition_rejects_non_frozenset_after():

    with pytest.raises(
        TypeError,
        match="after must be a frozenset",
    ):
        ObservationTransition(
            before=frozenset(),
            after=set(),
        )


def test_observation_transition_rejects_invalid_observations():

    with pytest.raises(
        TypeError,
        match="before and after must contain only",
    ):
        ObservationTransition(
            before=frozenset({
                "invalid",
            }),
            after=frozenset(),
        )


def test_observation_feedback_verifies_expected_post_action_state():

    before = frozenset({
        _observation(
            "environment",
            "file",
            "project",
            "old_state",
        ),
    })

    expected_observation = _observation(
        "environment",
        "file",
        "project",
        "new_state",
    )

    after = frozenset({
        expected_observation,
    })

    expected = ExpectedOutcome(
        observations=frozenset({
            expected_observation,
        }),
    )

    result = ObservationFeedback().evaluate(
        before=before,
        after=after,
        expected=expected,
    )

    assert isinstance(
        result,
        FeedbackResult,
    )

    assert result.status == "verified"
    assert result.expected == expected.observations
    assert result.observed == after


def test_observation_feedback_returns_unknown_when_expected_state_is_missing():

    before = frozenset({
        _observation(
            "environment",
            "file",
            "project",
            "old_state",
        ),
    })

    expected_observation = _observation(
        "environment",
        "file",
        "project",
        "new_state",
    )

    after = frozenset()

    expected = ExpectedOutcome(
        observations=frozenset({
            expected_observation,
        }),
    )

    result = ObservationFeedback().evaluate(
        before=before,
        after=after,
        expected=expected,
    )

    assert result.status == "unknown"


def test_before_observations_do_not_count_as_post_action_observations():

    expected_observation = _observation(
        "environment",
        "file",
        "project",
        "new_state",
    )

    before = frozenset({
        expected_observation,
    })

    after = frozenset()

    expected = ExpectedOutcome(
        observations=frozenset({
            expected_observation,
        }),
    )

    result = ObservationFeedback().evaluate(
        before=before,
        after=after,
        expected=expected,
    )

    assert result.status == "unknown"


def test_observation_feedback_uses_existing_feedback_evaluator():

    class RecordingEvaluator(FeedbackEvaluator):

        def __init__(self):
            self.expected = None
            self.observed = None

        def evaluate(
            self,
            expected,
            observed,
        ):
            self.expected = expected
            self.observed = observed

            return super().evaluate(
                expected,
                observed,
            )

    evaluator = RecordingEvaluator()

    expected_observation = _observation(
        "environment",
        "state",
        "project",
        "ready",
    )

    expected = ExpectedOutcome(
        observations=frozenset({
            expected_observation,
        }),
    )

    after = frozenset({
        expected_observation,
    })

    result = ObservationFeedback(
        evaluator=evaluator,
    ).evaluate(
        before=frozenset(),
        after=after,
        expected=expected,
    )

    assert evaluator.expected == expected
    assert evaluator.observed == after
    assert result.status == "verified"


def test_observation_feedback_does_not_modify_observations():

    before = frozenset({
        _observation(
            "environment",
            "state",
            "project",
            "before",
        ),
    })

    after = frozenset({
        _observation(
            "environment",
            "state",
            "project",
            "after",
        ),
    })

    expected = ExpectedOutcome(
        observations=after,
    )

    ObservationFeedback().evaluate(
        before=before,
        after=after,
        expected=expected,
    )

    assert before == frozenset({
        _observation(
            "environment",
            "state",
            "project",
            "before",
        ),
    })

    assert after == frozenset({
        _observation(
            "environment",
            "state",
            "project",
            "after",
        ),
    })


def test_observation_feedback_is_deterministic():

    observation = _observation(
        "environment",
        "state",
        "project",
        "ready",
    )

    expected = ExpectedOutcome(
        observations=frozenset({
            observation,
        }),
    )

    before = frozenset()

    after = frozenset({
        observation,
    })

    feedback = ObservationFeedback()

    first = feedback.evaluate(
        before=before,
        after=after,
        expected=expected,
    )

    second = feedback.evaluate(
        before=before,
        after=after,
        expected=expected,
    )

    assert first == second