from brain.environment.models.command_result import (
    CommandResult,
)

from brain.feedback.action_observation_orchestrator import (
    ActionObservationOrchestrator,
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


def test_successful_execution_and_verified_state_remain_distinct():
    expected_observation = _observation(
        "environment",
        "state",
        "project",
        "ready",
    )

    observations = iter(
        [
            frozenset(),
            frozenset({expected_observation}),
        ]
    )

    execution_result = CommandResult(
        return_code=0,
        stdout="success",
        stderr="",
    )

    expected = ExpectedOutcome(
        observations=frozenset(
            {expected_observation}
        ),
    )

    actual_execution_result, feedback_result = (
        ActionObservationOrchestrator(
            observe=lambda: next(observations),
            execute=lambda action: execution_result,
        ).execute(
            action="action",
            expected=expected,
        )
    )

    assert actual_execution_result == execution_result
    assert actual_execution_result.return_code == 0

    assert isinstance(
        feedback_result,
        FeedbackResult,
    )
    assert feedback_result.status == "verified"


def test_successful_execution_with_missing_state_is_unknown():
    expected_observation = _observation(
        "environment",
        "state",
        "project",
        "ready",
    )

    observations = iter(
        [
            frozenset(),
            frozenset(),
        ]
    )

    execution_result = CommandResult(
        return_code=0,
        stdout="success",
        stderr="",
    )

    expected = ExpectedOutcome(
        observations=frozenset(
            {expected_observation}
        ),
    )

    actual_execution_result, feedback_result = (
        ActionObservationOrchestrator(
            observe=lambda: next(observations),
            execute=lambda action: execution_result,
        ).execute(
            action="action",
            expected=expected,
        )
    )

    assert actual_execution_result.return_code == 0
    assert actual_execution_result.stdout == "success"
    assert feedback_result.status == "unknown"


def test_failed_execution_with_observed_state_preserves_both_signals():
    expected_observation = _observation(
        "environment",
        "state",
        "project",
        "changed",
    )

    observations = iter(
        [
            frozenset(),
            frozenset({expected_observation}),
        ]
    )

    execution_result = CommandResult(
        return_code=1,
        stdout="",
        stderr="reported failure",
    )

    expected = ExpectedOutcome(
        observations=frozenset(
            {expected_observation}
        ),
    )

    actual_execution_result, feedback_result = (
        ActionObservationOrchestrator(
            observe=lambda: next(observations),
            execute=lambda action: execution_result,
        ).execute(
            action="action",
            expected=expected,
        )
    )

    assert actual_execution_result.return_code == 1
    assert actual_execution_result.stderr == (
        "reported failure"
    )

    assert feedback_result.status == "verified"
    assert feedback_result.observed == frozenset(
        {expected_observation}
    )


def test_failed_execution_with_missing_state_remains_unknown():
    expected_observation = _observation(
        "environment",
        "state",
        "project",
        "changed",
    )

    observations = iter(
        [
            frozenset(),
            frozenset(),
        ]
    )

    execution_result = CommandResult(
        return_code=1,
        stdout="",
        stderr="command failed",
    )

    expected = ExpectedOutcome(
        observations=frozenset(
            {expected_observation}
        ),
    )

    actual_execution_result, feedback_result = (
        ActionObservationOrchestrator(
            observe=lambda: next(observations),
            execute=lambda action: execution_result,
        ).execute(
            action="action",
            expected=expected,
        )
    )

    assert actual_execution_result.return_code == 1
    assert actual_execution_result.stderr == (
        "command failed"
    )

    assert feedback_result.status == "unknown"
    assert feedback_result.observed == frozenset()


def test_execution_result_is_not_reinterpreted_by_feedback():
    observations = iter(
        [
            frozenset(),
            frozenset(),
        ]
    )

    execution_result = CommandResult(
        return_code=42,
        stdout="output",
        stderr="error",
    )

    expected = ExpectedOutcome(
        observations=frozenset(),
    )

    actual_execution_result, feedback_result = (
        ActionObservationOrchestrator(
            observe=lambda: next(observations),
            execute=lambda action: execution_result,
        ).execute(
            action="action",
            expected=expected,
        )
    )

    assert actual_execution_result == execution_result
    assert actual_execution_result.return_code == 42
    assert actual_execution_result.stdout == "output"
    assert actual_execution_result.stderr == "error"

    assert feedback_result.status == "verified"


def test_feedback_result_is_not_reinterpreted_by_execution_result():
    expected_observation = _observation(
        "environment",
        "state",
        "project",
        "ready",
    )

    observations = iter(
        [
            frozenset(),
            frozenset({expected_observation}),
        ]
    )

    execution_result = CommandResult(
        return_code=42,
        stdout="",
        stderr="execution error",
    )

    expected = ExpectedOutcome(
        observations=frozenset(
            {expected_observation}
        ),
    )

    actual_execution_result, feedback_result = (
        ActionObservationOrchestrator(
            observe=lambda: next(observations),
            execute=lambda action: execution_result,
        ).execute(
            action="action",
            expected=expected,
        )
    )

    assert actual_execution_result.return_code == 42
    assert actual_execution_result.stderr == (
        "execution error"
    )

    assert feedback_result.status == "verified"
    assert feedback_result.expected == frozenset(
        {expected_observation}
    )
    assert feedback_result.observed == frozenset(
        {expected_observation}
    )