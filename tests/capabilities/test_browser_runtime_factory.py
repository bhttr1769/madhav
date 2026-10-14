
from unittest.mock import MagicMock

import pytest

from brain.browser.interactive import browser_capability as browser_module
from brain.browser.interactive.browser_capability import BrowserCapability
from brain.capabilities.browser_runtime_factory import (
    create_browser_capability_runtime,
)
from brain.capabilities.capability_runtime import CapabilityRuntime
from brain.safety.services.safety_service import SafetyService


def test_factory_composes_browser_runtime_with_safety(
    monkeypatch,
):
    browser = BrowserCapability()
    monkeypatch.setattr(
        browser_module,
        "browser_capability",
        browser,
    )

    safety_service = MagicMock(spec=SafetyService)

    runtime = create_browser_capability_runtime(
        safety_service
    )

    assert isinstance(runtime, CapabilityRuntime)
    assert browser._safety_service is safety_service

    executor = runtime._executor
    descriptor = executor._registry.get(
        BrowserCapability.CAPABILITY_ID
    )

    assert descriptor == browser.capability_descriptor()


def test_factory_rejects_invalid_safety_service():
    with pytest.raises(
        TypeError,
        match="safety_service must be a SafetyService",
    ):
        create_browser_capability_runtime(object())
