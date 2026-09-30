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


def test_successful_execution_and_verified_state_are_both_preserved():

    expected_observation = _observation(
        "environment",
        "state",
        "project",
        "ready",
    )

    observations = iter([
        frozenset(),
        frozenset({
            expected_observation,
        }),
    ])

    execution_result = CommandResult(
        return_code=0,
        stdout="success",
        stderr="",
    )

    expected = ExpectedOutcome(
        observations=frozenset({
            expected_observation,
        }),
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

    assert isinstance(
        feedback_result,
        FeedbackResult,
    )

    assert feedback_result.status == "verified"


def test_failed_execution_result_is_preserved():

    observations = iter([
        frozenset(),
        frozenset(),
    ])

    execution_result = CommandResult(
        return_code=1,
        stdout="",
        stderr="command failed",
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
    assert actual_execution_result.return_code == 1
    assert actual_execution_result.stderr == "command failed"

    # Execution failure and state feedback remain
    # separate signals.
    assert feedback_result.status == "verified"


def test_successful_execution_does_not_imply_state_verification():

    expected_observation = _observation(
        "environment",
        "state",
        "project",
        "ready",
    )

    observations = iter([
        frozenset(),
        frozenset(),
    ])

    execution_result = CommandResult(
        return_code=0,
        stdout="success",
        stderr="",
    )

    expected = ExpectedOutcome(
        observations=frozenset({
            expected_observation,
        }),
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

    # The command succeeded, but the expected environmental
    # state was not observed.
    assert feedback_result.status == "unknown"


def test_failed_execution_does_not_hide_observed_state():

    expected_observation = _observation(
        "environment",
        "state",
        "project",
        "changed",
    )

    observations = iter([
        frozenset(),
        frozenset({
            expected_observation,
        }),
    ])

    execution_result = CommandResult(
        return_code=1,
        stdout="",
        stderr="reported failure",
    )

    expected = ExpectedOutcome(
        observations=frozenset({
            expected_observation,
        }),
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

    # The observed state is still independently evaluated.
    assert feedback_result.status == "verified"
    assert feedback_result.observed == frozenset({
        expected_observation,
    })


def test_execution_result_and_feedback_result_are_independent():

    expected_observation = _observation(
        "environment",
        "state",
        "project",
        "ready",
    )

    observations = iter([
        frozenset(),
        frozenset(),
    ])

    execution_result = CommandResult(
        return_code=0,
        stdout="success",
        stderr="",
    )

    expected = ExpectedOutcome(
        observations=frozenset({
            expected_observation,
        }),
    )

    execution, feedback = (
        ActionObservationOrchestrator(
            observe=lambda: next(observations),
            execute=lambda action: execution_result,
        ).execute(
            action="action",
            expected=expected,
        )
    )

    assert execution == execution_result
    assert feedback.status == "unknown"


def test_execution_result_is_not_reinterpreted_by_feedback():

    observations = iter([
        frozenset(),
        frozenset(),
    ])

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

    assert actual_execution_result.return_code == 42
    assert actual_execution_result.stdout == "output"
    assert actual_execution_result.stderr == "error"

    # Feedback must not transform or overwrite the execution result.
    assert feedback_result.expected == frozenset()
    assert feedback_result.observed == frozenset()