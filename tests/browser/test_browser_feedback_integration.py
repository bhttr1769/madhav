from unittest.mock import MagicMock

from brain.browser.interactive.browser_observation_builder import (
    BrowserObservationBuilder,
)
from brain.browser.interactive.models.browser_observation import (
    BrowserObservation,
)
from brain.feedback.action_observation_orchestrator import (
    ActionObservationOrchestrator,
)
from brain.feedback.models.expected_outcome import ExpectedOutcome
from brain.perception.models.observation import Observation


def test_browser_observation_integrates_with_feedback_orchestrator():
    builder = BrowserObservationBuilder()

    before = BrowserObservation(
        url="https://example.com",
        title="Example",
        text="Before",
    )

    after = BrowserObservation(
        url="https://example.com",
        title="Example",
        text="After",
    )

    observe_results = iter(
        [
            builder.build(before),
            builder.build(after),
        ]
    )

    observe = MagicMock(
        side_effect=lambda: next(observe_results)
    )

    execute = MagicMock(
        return_value="executed"
    )

    expected = ExpectedOutcome(
        observations=frozenset(
            {
                Observation(
                    source="browser",
                    category="text",
                    subject="page",
                    value="After",
                )
            }
        )
    )

    orchestrator = ActionObservationOrchestrator(
        observe=observe,
        execute=execute,
    )

    execution_result, feedback_result = (
        orchestrator.execute(
            action="browser-action",
            expected=expected,
        )
    )

    assert execution_result == "executed"
    assert feedback_result.status == "verified"
    assert observe.call_count == 2
    execute.assert_called_once_with(
        "browser-action"
    )