import pytest

from brain.feedback.action_observation_orchestrator import (
    ActionObservationOrchestrator,
)

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


def test_orchestrator_observes_before_and_after_execution():

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

    observations = iter([
        before,
        after,
    ])

    execution_calls = []

    def observe():
        return next(observations)

    def execute(action):
        execution_calls.append(action)
        return "execution-result"

    expected = ExpectedOutcome(
        observations=after,
    )

    result = ActionObservationOrchestrator(
        observe=observe,
        execute=execute,
    ).execute(
        action="test-action",
        expected=expected,
    )

    execution_result, feedback_result = result

    assert execution_result == "execution-result"
    assert isinstance(
        feedback_result,
        FeedbackResult,
    )

    assert feedback_result.status == "verified"
    assert execution_calls == [
        "test-action",
    ]


def test_orchestrator_calls_observation_before_execution():

    events = []

    before = frozenset()
    after = frozenset()

    observations = iter([
        before,
        after,
    ])

    def observe():
        events.append("observe")
        return next(observations)

    def execute(action):
        events.append("execute")
        return "result"

    expected = ExpectedOutcome(
        observations=frozenset(),
    )

    ActionObservationOrchestrator(
        observe=observe,
        execute=execute,
    ).execute(
        action="action",
        expected=expected,
    )

    assert events == [
        "observe",
        "execute",
        "observe",
    ]


def test_orchestrator_executes_action_exactly_once():

    calls = []

    def observe():
        return frozenset()

    def execute(action):
        calls.append(action)
        return "result"

    expected = ExpectedOutcome(
        observations=frozenset(),
    )

    ActionObservationOrchestrator(
        observe=observe,
        execute=execute,
    ).execute(
        action="action",
        expected=expected,
    )

    assert calls == [
        "action",
    ]


def test_orchestrator_returns_execution_result():

    def observe():
        return frozenset()

    def execute(action):
        return {
            "return_code": 0,
            "stdout": "success",
        }

    expected = ExpectedOutcome(
        observations=frozenset(),
    )

    execution_result, _ = (
        ActionObservationOrchestrator(
            observe=observe,
            execute=execute,
        ).execute(
            action="action",
            expected=expected,
        )
    )

    assert execution_result == {
        "return_code": 0,
        "stdout": "success",
    }


def test_orchestrator_returns_feedback_result():

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

    expected = ExpectedOutcome(
        observations=frozenset({
            expected_observation,
        }),
    )

    _, feedback_result = (
        ActionObservationOrchestrator(
            observe=lambda: next(observations),
            execute=lambda action: "result",
        ).execute(
            action="action",
            expected=expected,
        )
    )

    assert isinstance(
        feedback_result,
        FeedbackResult,
    )

    assert feedback_result.status == "verified"
    assert feedback_result.observed == frozenset({
        expected_observation,
    })


def test_orchestrator_returns_unknown_when_expected_state_is_missing():

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

    expected = ExpectedOutcome(
        observations=frozenset({
            expected_observation,
        }),
    )

    _, feedback_result = (
        ActionObservationOrchestrator(
            observe=lambda: next(observations),
            execute=lambda action: "result",
        ).execute(
            action="action",
            expected=expected,
        )
    )

    assert feedback_result.status == "unknown"


def test_orchestrator_reuses_existing_feedback_component():

    class RecordingFeedback(
        ObservationFeedback,
    ):

        def __init__(self):
            self.before = None
            self.after = None
            self.expected = None

        def evaluate(
            self,
            before,
            after,
            expected,
        ):
            self.before = before
            self.after = after
            self.expected = expected

            return FeedbackResult(
                status="verified",
                expected=expected.observations,
                observed=after,
            )

    feedback = RecordingFeedback()

    before = frozenset()
    after = frozenset()

    observations = iter([
        before,
        after,
    ])

    expected = ExpectedOutcome(
        observations=frozenset(),
    )

    ActionObservationOrchestrator(
        observe=lambda: next(observations),
        execute=lambda action: "result",
        feedback=feedback,
    ).execute(
        action="action",
        expected=expected,
    )

    assert feedback.before == before
    assert feedback.after == after
    assert feedback.expected == expected


def test_orchestrator_rejects_invalid_expected_outcome():

    orchestrator = ActionObservationOrchestrator(
        observe=lambda: frozenset(),
        execute=lambda action: "result",
    )

    with pytest.raises(
        TypeError,
        match="expected must be an ExpectedOutcome",
    ):
        orchestrator.execute(
            action="action",
            expected="invalid",
        )


def test_orchestrator_rejects_invalid_observation_result():

    orchestrator = ActionObservationOrchestrator(
        observe=lambda: [],
        execute=lambda action: "result",
    )

    expected = ExpectedOutcome(
        observations=frozenset(),
    )

    with pytest.raises(
        TypeError,
        match="observe must return a frozenset",
    ):
        orchestrator.execute(
            action="action",
            expected=expected,
        )


def test_orchestrator_rejects_invalid_observation_contents():

    orchestrator = ActionObservationOrchestrator(
        observe=lambda: frozenset({
            "invalid",
        }),
        execute=lambda action: "result",
    )

    expected = ExpectedOutcome(
        observations=frozenset(),
    )

    with pytest.raises(
        TypeError,
        match="containing only Observation instances",
    ):
        orchestrator.execute(
            action="action",
            expected=expected,
        )


def test_orchestrator_rejects_non_callable_observe():

    with pytest.raises(
        TypeError,
        match="observe must be callable",
    ):
        ActionObservationOrchestrator(
            observe="invalid",
            execute=lambda action: "result",
        )


def test_orchestrator_rejects_non_callable_execute():

    with pytest.raises(
        TypeError,
        match="execute must be callable",
    ):
        ActionObservationOrchestrator(
            observe=lambda: frozenset(),
            execute="invalid",
        )


def test_orchestrator_rejects_invalid_feedback():

    with pytest.raises(
        TypeError,
        match="feedback must be an ObservationFeedback",
    ):
        ActionObservationOrchestrator(
            observe=lambda: frozenset(),
            execute=lambda action: "result",
            feedback="invalid",
        )


def test_orchestrator_is_deterministic():

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

    def create_orchestrator():
        observations = iter([
            frozenset(),
            frozenset({
                observation,
            }),
        ])

        return ActionObservationOrchestrator(
            observe=lambda: next(observations),
            execute=lambda action: "result",
        )

    first = create_orchestrator().execute(
        action="action",
        expected=expected,
    )

    second = create_orchestrator().execute(
        action="action",
        expected=expected,
    )

    assert first == second