
from unittest.mock import MagicMock

import pytest

import brain.browser.interactive.browser_capability as browser_module
from brain.browser.interactive.browser_capability import BrowserCapability
from brain.browser.interactive.browser_session import BrowserSession
from brain.browser.interactive.safety_browser_action_executor import (
    SafetyBrowserActionExecutor,
)
from brain.safety.services.safety_service import SafetyService


def test_unconfigured_capability_fails_closed():
    capability = BrowserCapability()

    with pytest.raises(
        RuntimeError,
        match="safety service is not configured",
    ):
        capability._ensure_executor()


def test_configuration_updates_registered_capability_instance(
    monkeypatch,
):
    capability = BrowserCapability()
    capability._session = MagicMock(spec=BrowserSession)

    fake_browser_executor = MagicMock()
    monkeypatch.setattr(
        browser_module,
        "PlaywrightBrowserExecutor",
        lambda session: fake_browser_executor,
    )
    monkeypatch.setattr(
        browser_module,
        "browser_capability",
        capability,
    )

    safety_service = MagicMock(spec=SafetyService)

    configured = browser_module.configure_browser_capability(
        safety_service
    )

    assert configured is capability
    assert configured._safety_service is safety_service

    executor = configured._ensure_executor()

    assert isinstance(executor, SafetyBrowserActionExecutor)
    assert executor._safety_service is safety_service


def test_configuration_rejects_invalid_safety_service():
    capability = BrowserCapability()

    with pytest.raises(
        TypeError,
        match="safety_service must be a SafetyService",
    ):
        capability.configure_safety_service(object())


def test_configuration_cannot_replace_existing_safety_service():
    capability = BrowserCapability()
    first_service = MagicMock(spec=SafetyService)
    second_service = MagicMock(spec=SafetyService)

    capability.configure_safety_service(first_service)

    with pytest.raises(
        RuntimeError,
        match="already configured",
    ):
        capability.configure_safety_service(second_service)


def test_configuration_cannot_change_service_after_executor_initialization():
    capability = BrowserCapability()
    capability._executor = MagicMock(
        spec=SafetyBrowserActionExecutor
    )

    with pytest.raises(
        RuntimeError,
        match="after browser executor initialization",
    ):
        capability.configure_safety_service(
            MagicMock(spec=SafetyService)
        )
