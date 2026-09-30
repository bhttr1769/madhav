import pytest

from brain.feedback.action_observation_orchestrator import (
    ActionObservationOrchestrator,
)
from brain.feedback.models.expected_outcome import ExpectedOutcome
from brain.perception.ui_observation_builder import UIObservationBuilder
from brain.perception.models.observation import Observation
from brain.ui.executors.safety_ui_action_executor import (
    SafetyUIActionExecutor,
)
from brain.ui.executors.ui_action_executor import UIActionExecutor
from brain.ui.models.screen import Screen
from brain.ui.models.screen_understanding import ScreenUnderstanding
from brain.ui.models.ui_action import UIAction


class FakeSafetyService:

    def __init__(self):
        self.authorized_actions = []

    def authorize(self, action, approval=None):
        self.authorized_actions.append(
            (action, approval)
        )


class FakeUIExecutor(UIActionExecutor):

    def __init__(self):
        self.executed_actions = []

    def execute(self, action):
        self.executed_actions.append(action)


class FakeLoggingService:

    def __init__(self):
        self.calls = []

    def log(
        self,
        action,
        event,
        status,
        metadata=None,
    ):
        self.calls.append(
            {
                "action": action,
                "event": event,
                "status": status,
                "metadata": metadata,
            }
        )


def create_screen_understanding(
    window_title,
    text,
):
    screen = Screen(
        width=1920,
        height=1080,
    )

    from brain.ui.models.ui_element import UIElement

    element = UIElement(
        element_type="text",
        name="status",
        x=100,
        y=100,
        width=200,
        height=40,
        text=text,
        confidence=1.0,
    )

    return ScreenUnderstanding(
        screen=screen,
        elements=frozenset({element}),
        application="TestApplication",
        window_title=window_title,
    )


def create_safety_executor(
    fake_executor,
    safety_service,
):
    wrapper = object.__new__(
        SafetyUIActionExecutor
    )

    wrapper._safety_service = safety_service
    wrapper._executor = fake_executor
    wrapper._logging_service = FakeLoggingService()

    return wrapper


def test_ui_capability_full_validation():

    states = [
        create_screen_understanding(
            "Before",
            "Ready",
        ),
        create_screen_understanding(
            "After",
            "Completed",
        ),
    ]

    state_index = 0
    observation_builder = UIObservationBuilder()

    def observe():

        nonlocal state_index

        understanding = states[state_index]
        state_index += 1

        return observation_builder.build(
            understanding
        )

    safety_service = FakeSafetyService()
    ui_executor = FakeUIExecutor()

    safety_executor = create_safety_executor(
        fake_executor=ui_executor,
        safety_service=safety_service,
    )

    action = UIAction(
        action_type="click",
        x=100,
        y=200,
    )

    expected = ExpectedOutcome(
        observations=frozenset(
            {
                Observation(
                    source="ui",
                    category="window",
                    subject="screen",
                    value="After",
                ),
                Observation(
                    source="ui",
                    category="text",
                    subject="text:status:100:100:200:40",
                    value="Completed",
                ),
            }
        )
    )

    orchestrator = ActionObservationOrchestrator(
        observe=observe,
        execute=safety_executor.execute,
    )

    execution_result, feedback_result = (
        orchestrator.execute(
            action=action,
            expected=expected,
        )
    )

    assert execution_result is None

    assert feedback_result.status == "verified"

    assert ui_executor.executed_actions == [
        action
    ]

    assert len(
        safety_service.authorized_actions
    ) == 1

    assert safety_service.authorized_actions[
        0
    ][0] == action.to_action()


def test_safety_denial_prevents_ui_execution():

    class DenyingSafetyService:

        def authorize(
            self,
            action,
            approval=None,
        ):
            raise PermissionError(
                "UI action denied"
            )

    ui_executor = FakeUIExecutor()

    safety_executor = create_safety_executor(
        fake_executor=ui_executor,
        safety_service=DenyingSafetyService(),
    )

    action = UIAction(
        action_type="click",
        x=100,
        y=200,
    )

    with pytest.raises(
        PermissionError,
        match="UI action denied",
    ):
        safety_executor.execute(action)

    assert ui_executor.executed_actions == []