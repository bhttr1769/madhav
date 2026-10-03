from unittest.mock import MagicMock

import pytest

from brain.browser.interactive.browser_executor import BrowserExecutor
from brain.browser.interactive.models.browser_action import BrowserAction
from brain.browser.interactive.models.browser_element import BrowserElement
from brain.browser.interactive.safety_browser_action_executor import (
    SafetyBrowserActionExecutor,
)
from brain.safety.models.action import Action


def create_action():
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


def test_browser_action_converts_to_safety_action():
    action = create_action()

    safety_action = action.to_action()

    assert isinstance(safety_action, Action)
    assert safety_action.name == "click"
    assert safety_action.category == "browser"
    assert safety_action.target == "button:nth-of-type(1)"


def test_navigate_action_converts_to_safety_action():
    action = BrowserAction(
        action_type="navigate",
        url="https://example.com",
    )

    safety_action = action.to_action()

    assert safety_action.name == "navigate"
    assert safety_action.category == "browser"
    assert safety_action.target == "https://example.com"


def test_authorization_happens_before_execution():
    safety_service = MagicMock()
    executor = MagicMock(spec=BrowserExecutor)

    wrapper = SafetyBrowserActionExecutor(
        safety_service=safety_service,
        executor=executor,
    )

    action = create_action()

    wrapper.execute(action)

    safety_service.authorize.assert_called_once_with(
        action.to_action(),
        None,
    )
    executor.execute.assert_called_once_with(action)


def test_execution_does_not_happen_when_authorization_fails():
    safety_service = MagicMock()
    safety_service.authorize.side_effect = PermissionError(
        "Action is not authorized."
    )

    executor = MagicMock(spec=BrowserExecutor)

    wrapper = SafetyBrowserActionExecutor(
        safety_service=safety_service,
        executor=executor,
    )

    action = create_action()

    with pytest.raises(
        PermissionError,
        match="Action is not authorized",
    ):
        wrapper.execute(action)

    executor.execute.assert_not_called()


def test_approval_is_forwarded_to_safety_service():
    safety_service = MagicMock()
    executor = MagicMock(spec=BrowserExecutor)

    wrapper = SafetyBrowserActionExecutor(
        safety_service=safety_service,
        executor=executor,
    )

    action = create_action()

    from brain.safety.models.approval_response import ApprovalResponse

    wrapper.execute(
        action,
        ApprovalResponse.APPROVE,
    )

    safety_service.authorize.assert_called_once_with(
        action.to_action(),
        ApprovalResponse.APPROVE,
    )


def test_invalid_action_is_rejected():
    safety_service = MagicMock()
    executor = MagicMock(spec=BrowserExecutor)

    wrapper = SafetyBrowserActionExecutor(
        safety_service=safety_service,
        executor=executor,
    )

    with pytest.raises(
        TypeError,
        match="action must be a BrowserAction",
    ):
        wrapper.execute(MagicMock())