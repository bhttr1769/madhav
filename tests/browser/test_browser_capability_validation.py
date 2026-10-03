from unittest.mock import MagicMock

import pytest

from brain.browser.interactive.browser_capability import (
    BrowserCapability,
    browser_capability,
)
from brain.browser.interactive.browser_session import BrowserSession
from brain.browser.interactive.models.browser_observation import (
    BrowserObservation,
)
from brain.browser.interactive.models.browser_session_state import (
    BrowserSessionState,
)
from brain.browser.interactive.safety_browser_action_executor import (
    SafetyBrowserActionExecutor,
)
from brain.capabilities.capability_discovery import (
    CapabilityDiscovery,
)
from brain.capabilities.capability_executor import (
    CapabilityExecutor,
)
from brain.capabilities.capability_integrator import (
    CapabilityIntegrator,
)
from brain.capabilities.capability_registry import (
    CapabilityRegistry,
)
from brain.capabilities.capability_runtime import (
    CapabilityRuntime,
)
from brain.capabilities.entry_point_resolver import (
    EntryPointResolver,
)
from brain.capabilities.models.capability_execution_request import (
    CapabilityExecutionRequest,
)
from brain.capabilities.models.capability_execution_result import (
    CapabilityExecutionResult,
)
from brain.capabilities.models.capability_descriptor import (
    CapabilityDescriptor,
)
from brain.safety.services.safety_service import SafetyService


class FakeBrowserSession(BrowserSession):
    def __init__(self):
        self.active = False
        self.url = None
        self.start_count = 0
        self.close_count = 0
        self.navigate_calls = []
        self.observe_count = 0

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
    def __init__(self, session):
        self._session = session
        self.executed_actions = []

    def execute(self, action, approval=None):
        self.executed_actions.append(
            (action, approval)
        )

        if action.action_type == "navigate":
            self._session.navigate(action.url)


class FakeResolver:
    def __init__(self, implementation):
        self._implementation = implementation
        self.calls = []

    def resolve(self, entry_point):
        self.calls.append(entry_point)
        return self._implementation


def create_browser_capability():
    session = FakeBrowserSession()

    safety_service = MagicMock(
        spec=SafetyService
    )

    action_executor = (
        FakeSafetyBrowserActionExecutor(
            session
        )
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


def test_browser_capability_descriptor_is_discoverable():
    capability, _, _, _ = (
        create_browser_capability()
    )

    discovery = CapabilityDiscovery(
        providers=(capability,)
    )

    discovered = discovery.discover()

    assert discovered == (
        capability.capability_descriptor(),
    )

    descriptor = discovered[0]

    assert descriptor.id == (
        "browser.interactive"
    )

    assert descriptor.input_contract == (
        "browser_command"
    )

    assert descriptor.output_contract == (
        "browser_result"
    )


def test_browser_capability_entry_point_resolves():
    descriptor = (
        browser_capability.capability_descriptor()
    )

    resolver = EntryPointResolver()

    implementation = resolver.resolve(
        descriptor.entry_point
    )

    assert implementation is browser_capability


def test_browser_capability_can_be_integrated():
    capability, _, _, _ = (
        create_browser_capability()
    )

    descriptor = (
        capability.capability_descriptor()
    )

    registry = CapabilityRegistry()

    integrator = CapabilityIntegrator(
        registry
    )

    integrator.integrate(
        descriptor,
        verification_passed=True,
    )

    assert registry.has(
        "browser.interactive"
    )

    assert registry.get(
        "browser.interactive"
    ) == descriptor


def test_browser_capability_cannot_be_integrated_without_verification():
    capability, _, _, _ = (
        create_browser_capability()
    )

    descriptor = (
        capability.capability_descriptor()
    )

    registry = CapabilityRegistry()

    integrator = CapabilityIntegrator(
        registry
    )

    with pytest.raises(
        ValueError,
        match="cannot integrate an unverified capability",
    ):
        integrator.integrate(
            descriptor,
            verification_passed=False,
        )

    assert registry.has(
        "browser.interactive"
    ) is False


def test_browser_capability_executes_through_capability_executor():
    capability, session, _, _ = (
        create_browser_capability()
    )

    descriptor = (
        capability.capability_descriptor()
    )

    registry = CapabilityRegistry(
        capabilities=(descriptor,)
    )

    resolver = FakeResolver(
        capability
    )

    executor = CapabilityExecutor(
        registry=registry,
        resolver=resolver,
    )

    result = executor.execute(
        capability_id="browser.interactive",
        input_data={
            "operation": "start"
        },
    )

    assert result.active is True
    assert session.start_count == 1

    assert resolver.calls == [
        descriptor.entry_point
    ]


def test_browser_capability_executes_through_runtime():
    capability, session, _, _ = (
        create_browser_capability()
    )

    descriptor = (
        capability.capability_descriptor()
    )

    registry = CapabilityRegistry(
        capabilities=(descriptor,)
    )

    resolver = FakeResolver(
        capability
    )

    executor = CapabilityExecutor(
        registry=registry,
        resolver=resolver,
    )

    runtime = CapabilityRuntime(
        executor
    )

    request = CapabilityExecutionRequest(
        capability_id="browser.interactive",
        input_data={
            "operation": "start"
        },
    )

    result = runtime.execute(
        request
    )

    assert isinstance(
        result,
        CapabilityExecutionResult,
    )

    assert result.capability_id == (
        "browser.interactive"
    )

    assert result.output.active is True
    assert session.active is True


def test_browser_capability_preserves_state_through_runtime():
    capability, session, _, _ = (
        create_browser_capability()
    )

    descriptor = (
        capability.capability_descriptor()
    )

    registry = CapabilityRegistry(
        capabilities=(descriptor,)
    )

    resolver = FakeResolver(
        capability
    )

    executor = CapabilityExecutor(
        registry=registry,
        resolver=resolver,
    )

    runtime = CapabilityRuntime(
        executor
    )

    runtime.execute(
        CapabilityExecutionRequest(
            capability_id=(
                "browser.interactive"
            ),
            input_data={
                "operation": "start"
            },
        )
    )

    result = runtime.execute(
        CapabilityExecutionRequest(
            capability_id=(
                "browser.interactive"
            ),
            input_data={
                "operation": "navigate",
                "url": "https://example.com",
            },
        )
    )

    assert result.output.active is True
    assert result.output.url == (
        "https://example.com"
    )

    assert session.navigate_calls == [
        "https://example.com"
    ]


def test_browser_capability_observation_works_through_runtime():
    capability, session, _, _ = (
        create_browser_capability()
    )

    descriptor = (
        capability.capability_descriptor()
    )

    registry = CapabilityRegistry(
        capabilities=(descriptor,)
    )

    resolver = FakeResolver(
        capability
    )

    executor = CapabilityExecutor(
        registry=registry,
        resolver=resolver,
    )

    runtime = CapabilityRuntime(
        executor
    )

    runtime.execute(
        CapabilityExecutionRequest(
            capability_id=(
                "browser.interactive"
            ),
            input_data={
                "operation": "start"
            },
        )
    )

    runtime.execute(
        CapabilityExecutionRequest(
            capability_id=(
                "browser.interactive"
            ),
            input_data={
                "operation": "navigate",
                "url": "https://example.com",
            },
        )
    )

    result = runtime.execute(
        CapabilityExecutionRequest(
            capability_id=(
                "browser.interactive"
            ),
            input_data={
                "operation": "observe"
            },
        )
    )

    assert session.observe_count == 1

    assert any(
        observation.category == "url"
        and observation.value
        == "https://example.com"
        for observation in result.output
    )


def test_browser_capability_runtime_propagates_execution_failure():
    capability, _, _, _ = (
        create_browser_capability()
    )

    descriptor = (
        capability.capability_descriptor()
    )

    registry = CapabilityRegistry(
        capabilities=(descriptor,)
    )

    class FailingCapability:
        def execute(self, input_data):
            raise RuntimeError(
                "browser execution failed"
            )

    resolver = FakeResolver(
        FailingCapability()
    )

    executor = CapabilityExecutor(
        registry=registry,
        resolver=resolver,
    )

    runtime = CapabilityRuntime(
        executor
    )

    with pytest.raises(
        RuntimeError,
        match="browser execution failed",
    ):
        runtime.execute(
            CapabilityExecutionRequest(
                capability_id=(
                    "browser.interactive"
                ),
                input_data={
                    "operation": "start"
                },
            )
        )