from brain.feedback.feedback_evaluator import (
    FeedbackEvaluator,
)

from brain.feedback.models.expected_outcome import (
    ExpectedOutcome,
)

from brain.feedback.models.feedback_result import (
    FeedbackResult,
)

from brain.perception.models.observation import (
    Observation,
)


def _observation(
    value: str,
) -> Observation:

    return Observation(
        source="workspace",
        category="state",
        subject="project",
        value=value,
    )


def test_expected_outcome_accepts_observations():

    observation = _observation(
        "file_exists",
    )

    outcome = ExpectedOutcome(
        observations=frozenset({
            observation,
        }),
    )

    assert outcome.observations == frozenset({
        observation,
    })


def test_expected_outcome_is_immutable():

    outcome = ExpectedOutcome(
        observations=frozenset(),
    )

    try:
        outcome.observations = frozenset({
            _observation("file_exists"),
        })
    except AttributeError:
        pass
    else:
        raise AssertionError(
            "ExpectedOutcome must be immutable"
        )


def test_feedback_result_is_immutable():

    result = FeedbackResult(
        status="verified",
        expected=frozenset(),
        observed=frozenset(),
    )

    try:
        result.status = "unknown"
    except AttributeError:
        pass
    else:
        raise AssertionError(
            "FeedbackResult must be immutable"
        )


def test_exact_expected_observations_are_verified():

    expected_observation = _observation(
        "file_exists",
    )

    expected = ExpectedOutcome(
        observations=frozenset({
            expected_observation,
        }),
    )

    observed = frozenset({
        expected_observation,
    })

    result = FeedbackEvaluator().evaluate(
        expected,
        observed,
    )

    assert result.status == "verified"
    assert result.expected == expected.observations
    assert result.observed == observed


def test_expected_observations_subset_of_observed_is_verified():

    expected_observation = _observation(
        "file_exists",
    )

    additional_observation = _observation(
        "git_repository",
    )

    expected = ExpectedOutcome(
        observations=frozenset({
            expected_observation,
        }),
    )

    observed = frozenset({
        expected_observation,
        additional_observation,
    })

    result = FeedbackEvaluator().evaluate(
        expected,
        observed,
    )

    assert result.status == "verified"


def test_missing_expected_observation_is_unknown():

    expected_observation = _observation(
        "file_exists",
    )

    expected = ExpectedOutcome(
        observations=frozenset({
            expected_observation,
        }),
    )

    observed = frozenset()

    result = FeedbackEvaluator().evaluate(
        expected,
        observed,
    )

    assert result.status == "unknown"


def test_empty_expected_outcome_is_verified():

    expected = ExpectedOutcome(
        observations=frozenset(),
    )

    observed = frozenset({
        _observation("file_exists"),
    })

    result = FeedbackEvaluator().evaluate(
        expected,
        observed,
    )

    assert result.status == "verified"


def test_feedback_evaluation_is_deterministic():

    observation = _observation(
        "file_exists",
    )

    expected = ExpectedOutcome(
        observations=frozenset({
            observation,
        }),
    )

    observed = frozenset({
        observation,
    })

    evaluator = FeedbackEvaluator()

    first = evaluator.evaluate(
        expected,
        observed,
    )

    second = evaluator.evaluate(
        expected,
        observed,
    )

    assert first == second


def test_expected_outcome_rejects_invalid_observations():

    try:
        ExpectedOutcome(
            observations=frozenset({
                "invalid",
            }),
        )
    except TypeError:
        pass
    else:
        raise AssertionError(
            "ExpectedOutcome must reject invalid observations"
        )


def test_expected_outcome_rejects_non_frozenset():

    try:
        ExpectedOutcome(
            observations=set(),
        )
    except TypeError:
        pass
    else:
        raise AssertionError(
            "ExpectedOutcome must require a frozenset"
        )


def test_feedback_evaluator_rejects_invalid_expected():

    try:
        FeedbackEvaluator().evaluate(
            expected="invalid",
            observed=frozenset(),
        )
    except TypeError:
        pass
    else:
        raise AssertionError(
            "FeedbackEvaluator must reject invalid expected outcomes"
        )


def test_feedback_evaluator_rejects_non_frozenset_observed():

    expected = ExpectedOutcome(
        observations=frozenset(),
    )

    try:
        FeedbackEvaluator().evaluate(
            expected,
            observed=set(),
        )
    except TypeError:
        pass
    else:
        raise AssertionError(
            "FeedbackEvaluator must require a frozenset"
        )


def test_feedback_evaluator_rejects_invalid_observed():

    expected = ExpectedOutcome(
        observations=frozenset(),
    )

    try:
        FeedbackEvaluator().evaluate(
            expected,
            observed=frozenset({
                "invalid",
            }),
        )
    except TypeError:
        pass
    else:
        raise AssertionError(
            "FeedbackEvaluator must reject invalid observations"
        )