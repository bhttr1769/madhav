from brain.feedback.action_observation_orchestrator import (
    ActionObservationOrchestrator,
)
from brain.feedback.models.expected_outcome import ExpectedOutcome
from brain.feedback.models.feedback_result import FeedbackResult
from brain.perception.models.observation import Observation
from brain.ui.models.ui_action import UIAction


def test_ui_action_with_verified_observation():

    observations = [
        frozenset(
            {
                Observation(
                    source="ui",
                    category="window",
                    subject="screen",
                    value="Before",
                )
            }
        ),
        frozenset(
            {
                Observation(
                    source="ui",
                    category="window",
                    subject="screen",
                    value="After",
                )
            }
        ),
    ]

    observation_index = 0

    def observe():
        nonlocal observation_index

        result = observations[observation_index]
        observation_index += 1

        return result

    executed_actions = []

    def execute(action):
        executed_actions.append(action)
        return "executed"

    expected = ExpectedOutcome(
        observations=frozenset(
            {
                Observation(
                    source="ui",
                    category="window",
                    subject="screen",
                    value="After",
                )
            }
        )
    )

    orchestrator = ActionObservationOrchestrator(
        observe=observe,
        execute=execute,
    )

    action = UIAction(
        action_type="click",
        x=100,
        y=200,
    )

    execution_result, feedback_result = orchestrator.execute(
        action=action,
        expected=expected,
    )

    assert execution_result == "executed"
    assert feedback_result.status == "verified"
    assert executed_actions == [action]


def test_ui_action_with_unknown_observation():

    observations = [
        frozenset(
            {
                Observation(
                    source="ui",
                    category="window",
                    subject="screen",
                    value="Before",
                )
            }
        ),
        frozenset(
            {
                Observation(
                    source="ui",
                    category="window",
                    subject="screen",
                    value="Different",
                )
            }
        ),
    ]

    observation_index = 0

    def observe():
        nonlocal observation_index

        result = observations[observation_index]
        observation_index += 1

        return result

    def execute(action):
        return "executed"

    expected = ExpectedOutcome(
        observations=frozenset(
            {
                Observation(
                    source="ui",
                    category="window",
                    subject="screen",
                    value="After",
                )
            }
        )
    )

    orchestrator = ActionObservationOrchestrator(
        observe=observe,
        execute=execute,
    )

    action = UIAction(
        action_type="click",
        x=100,
        y=200,
    )

    execution_result, feedback_result = orchestrator.execute(
        action=action,
        expected=expected,
    )

    assert execution_result == "executed"
    assert feedback_result.status == "unknown"