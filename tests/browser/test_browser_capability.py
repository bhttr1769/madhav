from unittest.mock import MagicMock

import pytest

from brain.browser.interactive.browser_capability import (
    BrowserCapability,
)
from brain.browser.interactive.browser_session import BrowserSession
from brain.browser.interactive.browser_observation_builder import (
    BrowserObservationBuilder,
)
from brain.browser.interactive.models.browser_action import BrowserAction
from brain.browser.interactive.models.browser_element import BrowserElement
from brain.browser.interactive.models.browser_observation import (
    BrowserObservation,
)
from brain.browser.interactive.models.browser_session_state import (
    BrowserSessionState,
)
from brain.browser.interactive.safety_browser_action_executor import (
    SafetyBrowserActionExecutor,
)
from brain.capabilities.models.capability_descriptor import (
    CapabilityDescriptor,
)
from brain.safety.models.approval_response import ApprovalResponse
from brain.safety.services.safety_service import SafetyService


class FakeBrowserSession(BrowserSession):
    def __init__(self):
        self.start_count = 0
        self.close_count = 0
        self.navigate_calls = []
        self.observe_count = 0
        self.active = False
        self.url = None

    def start(self):
        self.start_count += 1
        self.active = True

    def close(self):
        self.close_count += 1
        self.active = False
        self.url = None

    def navigate(self, url):
        if not self.active:
            raise RuntimeError(
                "browser session is not active"
            )

        self.navigate_calls.append(url)
        self.url = url

    def current_state(self):
        return BrowserSessionState(
            active=self.active,
            url=self.url,
        )

    def observe(self):
        if not self.active:
            raise RuntimeError(
                "browser session is not active"
            )

        self.observe_count += 1

        return BrowserObservation(
            url=self.url,
            title="Example",
            text="Example page",
            elements=frozenset(),
        )


class FakeSafetyBrowserActionExecutor(
    SafetyBrowserActionExecutor
):
    """
    Test-only executor.

    It preserves the SafetyBrowserActionExecutor contract while
    delegating navigation to the fake browser session instead
    of touching Playwright internals.
    """

    def __init__(self, session):
        self._session = session
        self.executed_actions = []

    def execute(self, action, approval=None):
        self.executed_actions.append(
            (action, approval)
        )

        if action.action_type == "navigate":
            self._session.navigate(action.url)


def create_capability():
    session = FakeBrowserSession()
    safety_service = MagicMock(
        spec=SafetyService
    )

    action_executor = FakeSafetyBrowserActionExecutor(
        session
    )

    capability = BrowserCapability(
        session=session,
        safety_service=safety_service,
        action_executor=action_executor,
    )

    return (
        capability,
        session,
        safety_service,
        action_executor,
    )


def create_click_action():
    element = BrowserElement(
        element_type="button",
        name="Submit",
        text="Submit",
        selector="button:nth-of-type(1)",
        interactive=True,
    )

    return BrowserAction(
        action_type="click",
        target=element,
    )


def test_capability_descriptor_returns_descriptor():
    capability, _, _, _ = create_capability()

    descriptor = capability.capability_descriptor()

    assert isinstance(
        descriptor,
        CapabilityDescriptor,
    )

    assert descriptor.id == "browser.interactive"
    assert descriptor.name == "Interactive Browser"
    assert descriptor.version == "1.0.0"
    assert (
        descriptor.entry_point
        == (
            "brain.browser.interactive."
            "browser_capability.browser_capability"
        )
    )
    assert descriptor.dependencies == frozenset()
    assert descriptor.input_contract == "browser_command"
    assert descriptor.output_contract == "browser_result"


def test_start_starts_persistent_session():
    capability, session, _, _ = create_capability()

    result = capability.execute(
        {"operation": "start"}
    )

    assert result.active is True
    assert session.start_count == 1


def test_multiple_operations_reuse_same_session():
    (
        capability,
        session,
        _,
        action_executor,
    ) = create_capability()

    capability.execute(
        {"operation": "start"}
    )

    capability.execute(
        {
            "operation": "navigate",
            "url": "https://example.com",
        }
    )

    result = capability.execute(
        {"operation": "observe"}
    )

    assert session.start_count == 1
    assert session.navigate_calls == [
        "https://example.com"
    ]
    assert session.observe_count == 1

    assert any(
        observation.category == "url"
        and observation.value == "https://example.com"
        for observation in result
    )

    assert action_executor.executed_actions[0][0] == (
        BrowserAction(
            action_type="navigate",
            url="https://example.com",
        )
    )


def test_navigate_returns_state_from_session_after_execution():
    session = FakeBrowserSession()
    safety_service = MagicMock(
        spec=SafetyService
    )
    action_executor = FakeSafetyBrowserActionExecutor(
        session
    )

    capability = BrowserCapability(
        session=session,
        safety_service=safety_service,
        action_executor=action_executor,
    )

    capability.execute(
        {"operation": "start"}
    )

    result = capability.execute(
        {
            "operation": "navigate",
            "url": "https://example.com",
        }
    )

    assert result.active is True
    assert result.url == "https://example.com"


def test_observe_uses_existing_observation_builder():
    session = FakeBrowserSession()
    session.start()

    builder = MagicMock(
        spec=BrowserObservationBuilder
    )

    expected = frozenset()

    builder.build.return_value = expected

    capability = BrowserCapability(
        session=session,
        observation_builder=builder,
    )

    result = capability.execute(
        {"operation": "observe"}
    )

    assert result == expected
    builder.build.assert_called_once()

    observed = builder.build.call_args.args[0]

    assert isinstance(
        observed,
        BrowserObservation,
    )


def test_observe_returns_generic_observations():
    (
        capability,
        session,
        _,
        _,
    ) = create_capability()

    capability.execute(
        {"operation": "start"}
    )

    capability.execute(
        {
            "operation": "navigate",
            "url": "https://example.com",
        }
    )

    result = capability.execute(
        {"operation": "observe"}
    )

    assert any(
        observation.category == "url"
        and observation.value == "https://example.com"
        for observation in result
    )

    assert any(
        observation.category == "title"
        and observation.value == "Example"
        for observation in result
    )

    assert any(
        observation.category == "text"
        and observation.value == "Example page"
        for observation in result
    )


def test_action_requires_browser_action():
    capability, _, _, _ = create_capability()

    with pytest.raises(
        TypeError,
        match="action operation requires a BrowserAction",
    ):
        capability.execute(
            {
                "operation": "action",
                "action": object(),
            }
        )


def test_action_uses_safety_executor():
    session = FakeBrowserSession()
    safety_service = MagicMock(
        spec=SafetyService
    )

    capability = BrowserCapability(
        session=session,
        safety_service=safety_service,
    )

    capability.execute(
        {"operation": "start"}
    )

    action = create_click_action()

    capability._executor = MagicMock(
        spec=SafetyBrowserActionExecutor
    )

    capability.execute(
        {
            "operation": "action",
            "action": action,
        }
    )

    capability._executor.execute.assert_called_once_with(
        action,
        None,
    )


def test_action_forwards_approval():
    session = FakeBrowserSession()
    safety_service = MagicMock(
        spec=SafetyService
    )

    capability = BrowserCapability(
        session=session,
        safety_service=safety_service,
    )

    capability.execute(
        {"operation": "start"}
    )

    action = create_click_action()

    capability._executor = MagicMock(
        spec=SafetyBrowserActionExecutor
    )

    capability.execute(
        {
            "operation": "action",
            "action": action,
            "approval": ApprovalResponse.APPROVE,
        }
    )

    capability._executor.execute.assert_called_once_with(
        action,
        ApprovalResponse.APPROVE,
    )


def test_close_closes_existing_session():
    capability, session, _, _ = create_capability()

    capability.execute(
        {"operation": "start"}
    )

    result = capability.execute(
        {"operation": "close"}
    )

    assert session.close_count == 1
    assert result.active is False
    assert result.url is None


def test_close_without_session_is_safe():
    capability = BrowserCapability()

    result = capability.execute(
        {"operation": "close"}
    )

    assert result is None


def test_invalid_input_is_rejected():
    capability, _, _, _ = create_capability()

    with pytest.raises(
        TypeError,
        match="input_data must be a dict",
    ):
        capability.execute("start")


def test_missing_operation_is_rejected():
    capability, _, _, _ = create_capability()

    with pytest.raises(
        TypeError,
        match="operation must be a string",
    ):
        capability.execute({})


def test_empty_operation_is_rejected():
    capability, _, _, _ = create_capability()

    with pytest.raises(
        ValueError,
        match="operation must not be empty",
    ):
        capability.execute(
            {"operation": ""}
        )


def test_unsupported_operation_is_rejected():
    capability, _, _, _ = create_capability()

    with pytest.raises(
        ValueError,
        match="unsupported browser operation",
    ):
        capability.execute(
            {"operation": "delete"}
        )


def test_navigate_requires_string_url():
    capability, session, _, _ = create_capability()

    capability.execute(
        {"operation": "start"}
    )

    with pytest.raises(
        TypeError,
        match="navigate operation requires a string url",
    ):
        capability.execute(
            {
                "operation": "navigate",
                "url": 123,
            }
        )

    assert session.navigate_calls == []


def test_action_requires_safety_service():
    session = FakeBrowserSession()

    capability = BrowserCapability(
        session=session,
    )

    capability.execute(
        {"operation": "start"}
    )

    action = create_click_action()

    with pytest.raises(
        RuntimeError,
        match="safety service is not configured",
    ):
        capability.execute(
            {
                "operation": "action",
                "action": action,
            }
        )


def test_session_type_is_validated():
    with pytest.raises(
        TypeError,
        match="session must be a BrowserSession",
    ):
        BrowserCapability(
            session=object()
        )


def test_safety_service_type_is_validated():
    session = FakeBrowserSession()

    with pytest.raises(
        TypeError,
        match="safety_service must be a SafetyService",
    ):
        BrowserCapability(
            session=session,
            safety_service=object(),
        )


def test_observation_builder_type_is_validated():
    session = FakeBrowserSession()

    with pytest.raises(
        TypeError,
        match=(
            "observation_builder must be a "
            "BrowserObservationBuilder"
        ),
    ):
        BrowserCapability(
            session=session,
            observation_builder=object(),
        )


def test_capability_can_be_discovered_as_provider():
    capability, _, _, _ = create_capability()

    descriptor = capability.capability_descriptor()

    assert descriptor.id == capability.CAPABILITY_ID
    assert descriptor.entry_point.endswith(
        "browser_capability"
    )


def test_capability_preserves_session_state_across_calls():
    (
        capability,
        session,
        _,
        _,
    ) = create_capability()

    capability.execute(
        {"operation": "start"}
    )

    capability.execute(
        {
            "operation": "navigate",
            "url": "https://example.com",
        }
    )

    first_state = session.current_state()

    capability.execute(
        {"operation": "observe"}
    )

    second_state = session.current_state()

    assert first_state.active is True
    assert second_state.active is True

    assert (
        first_state.url
        == second_state.url
        == "https://example.com"
    )


def test_browser_action_is_not_executed_without_safety():
    session = FakeBrowserSession()
    safety_service = MagicMock(
        spec=SafetyService
    )

    safety_service.authorize.side_effect = (
        PermissionError(
            "Action is not authorized."
        )
    )

    capability = BrowserCapability(
        session=session,
        safety_service=safety_service,
    )

    capability.execute(
        {"operation": "start"}
    )

    action = create_click_action()

    with pytest.raises(
        PermissionError,
        match="Action is not authorized",
    ):
        capability.execute(
            {
                "operation": "action",
                "action": action,
            }
        )

    safety_service.authorize.assert_called_once_with(
        action.to_action(),
        None,
    )


def test_navigate_uses_safety_executor():
    session = FakeBrowserSession()
    safety_service = MagicMock(
        spec=SafetyService
    )

    capability = BrowserCapability(
        session=session,
        safety_service=safety_service,
    )

    capability.execute(
        {"operation": "start"}
    )

    capability._executor = MagicMock(
        spec=SafetyBrowserActionExecutor
    )

    result = capability.execute(
        {
            "operation": "navigate",
            "url": "https://example.com",
        }
    )

    expected_action = BrowserAction(
        action_type="navigate",
        url="https://example.com",
    )

    capability._executor.execute.assert_called_once_with(
        expected_action,
        None,
    )

    assert result.active is True


def test_navigate_forwards_approval():
    session = FakeBrowserSession()
    safety_service = MagicMock(
        spec=SafetyService
    )

    capability = BrowserCapability(
        session=session,
        safety_service=safety_service,
    )

    capability.execute(
        {"operation": "start"}
    )

    capability._executor = MagicMock(
        spec=SafetyBrowserActionExecutor
    )

    capability.execute(
        {
            "operation": "navigate",
            "url": "https://example.com",
            "approval": ApprovalResponse.APPROVE,
        }
    )

    expected_action = BrowserAction(
        action_type="navigate",
        url="https://example.com",
    )

    capability._executor.execute.assert_called_once_with(
        expected_action,
        ApprovalResponse.APPROVE,
    )


def test_navigation_does_not_execute_when_safety_fails():
    session = FakeBrowserSession()
    safety_service = MagicMock(
        spec=SafetyService
    )

    capability = BrowserCapability(
        session=session,
        safety_service=safety_service,
    )

    capability.execute(
        {"operation": "start"}
    )

    capability._executor = MagicMock(
        spec=SafetyBrowserActionExecutor
    )

    capability._executor.execute.side_effect = (
        PermissionError(
            "Action is not authorized."
        )
    )

    with pytest.raises(
        PermissionError,
        match="Action is not authorized",
    ):
        capability.execute(
            {
                "operation": "navigate",
                "url": "https://example.com",
            }
        )

    assert session.navigate_calls == []