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
    value: str,
) -> Observation:
    return Observation(
        source="environment",
        category="state",
        subject="project",
        value=value,
    )


def test_feedback_result_rejects_non_string_status():

    with pytest.raises(
        TypeError,
        match="status must be a string",
    ):
        FeedbackResult(
            status=123,
            expected=frozenset(),
            observed=frozenset(),
        )


def test_feedback_result_rejects_empty_status():

    with pytest.raises(
        ValueError,
        match="status must not be empty",
    ):
        FeedbackResult(
            status="",
            expected=frozenset(),
            observed=frozenset(),
        )


def test_feedback_result_rejects_non_frozenset_expected():

    with pytest.raises(
        TypeError,
        match="expected must be a frozenset",
    ):
        FeedbackResult(
            status="verified",
            expected=set(),
            observed=frozenset(),
        )


def test_feedback_result_rejects_non_frozenset_observed():

    with pytest.raises(
        TypeError,
        match="observed must be a frozenset",
    ):
        FeedbackResult(
            status="verified",
            expected=frozenset(),
            observed=set(),
        )


def test_feedback_result_rejects_invalid_expected_observation():

    with pytest.raises(
        TypeError,
        match="expected and observed must contain only",
    ):
        FeedbackResult(
            status="verified",
            expected=frozenset({"invalid"}),
            observed=frozenset(),
        )


def test_feedback_result_rejects_invalid_observed_observation():

    with pytest.raises(
        TypeError,
        match="expected and observed must contain only",
    ):
        FeedbackResult(
            status="verified",
            expected=frozenset(),
            observed=frozenset({"invalid"}),
        )


def test_feedback_result_accepts_valid_feedback():

    observation = _observation(
        "ready",
    )

    result = FeedbackResult(
        status="verified",
        expected=frozenset({observation}),
        observed=frozenset({observation}),
    )

    assert result.status == "verified"
    assert result.expected == frozenset({observation})
    assert result.observed == frozenset({observation})


def test_observation_feedback_rejects_invalid_before():

    expected = ExpectedOutcome(
        observations=frozenset(),
    )

    with pytest.raises(
        TypeError,
        match="before must be a frozenset",
    ):
        ObservationFeedback().evaluate(
            before=set(),
            after=frozenset(),
            expected=expected,
        )


def test_observation_feedback_rejects_invalid_after():

    expected = ExpectedOutcome(
        observations=frozenset(),
    )

    with pytest.raises(
        TypeError,
        match="after must be a frozenset",
    ):
        ObservationFeedback().evaluate(
            before=frozenset(),
            after=set(),
            expected=expected,
        )


def test_observation_feedback_rejects_invalid_before_observations():

    expected = ExpectedOutcome(
        observations=frozenset(),
    )

    with pytest.raises(
        TypeError,
        match="before and after must contain only",
    ):
        ObservationFeedback().evaluate(
            before=frozenset({"invalid"}),
            after=frozenset(),
            expected=expected,
        )


def test_observation_feedback_rejects_invalid_after_observations():

    expected = ExpectedOutcome(
        observations=frozenset(),
    )

    with pytest.raises(
        TypeError,
        match="before and after must contain only",
    ):
        ObservationFeedback().evaluate(
            before=frozenset(),
            after=frozenset({"invalid"}),
            expected=expected,
        )


def test_observation_feedback_rejects_invalid_expected():

    with pytest.raises(
        TypeError,
        match="expected must be an ExpectedOutcome",
    ):
        ObservationFeedback().evaluate(
            before=frozenset(),
            after=frozenset(),
            expected="invalid",
        )


def test_observation_feedback_preserves_valid_verified_result():

    observation = _observation(
        "ready",
    )

    expected = ExpectedOutcome(
        observations=frozenset({observation}),
    )

    result = ObservationFeedback().evaluate(
        before=frozenset(),
        after=frozenset({observation}),
        expected=expected,
    )

    assert result.status == (
        FeedbackEvaluator.VERIFIED
    )


def test_observation_feedback_preserves_valid_unknown_result():

    observation = _observation(
        "ready",
    )

    expected = ExpectedOutcome(
        observations=frozenset({observation}),
    )

    result = ObservationFeedback().evaluate(
        before=frozenset(),
        after=frozenset(),
        expected=expected,
    )

    assert result.status == (
        FeedbackEvaluator.UNKNOWN
    )


def test_observation_transition_remains_the_pre_post_boundary():

    before = frozenset({
        _observation("before"),
    })

    after = frozenset({
        _observation("after"),
    })

    transition = ObservationTransition(
        before=before,
        after=after,
    )

    assert transition.before == before
    assert transition.after == after