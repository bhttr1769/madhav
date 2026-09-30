import pytest

from brain.capabilities.capability_executor import CapabilityExecutor
from brain.capabilities.capability_registry import CapabilityRegistry
from brain.capabilities.capability_runtime import CapabilityRuntime
from brain.capabilities.models.capability_descriptor import (
    CapabilityDescriptor,
)
from brain.capabilities.models.capability_execution_request import (
    CapabilityExecutionRequest,
)
from brain.capabilities.models.capability_execution_result import (
    CapabilityExecutionResult,
)
from brain.capabilities.capability_integrator import CapabilityIntegrator


class TestCapability:
    @staticmethod
    def execute(input_data):
        return {
            "received": input_data,
        }

class FailingCapability:
    @staticmethod
    def execute(input_data):
        raise RuntimeError("capability failed")

class IntegratedCapability:
    @staticmethod
    def execute(input_data):
        return {
            "processed": input_data,
        }


def _capability():
    return CapabilityDescriptor(
        id="test.capability",
        name="Test Capability",
        description="Test capability.",
        version="1.0.0",
        entry_point=(
            "tests.capabilities.test_capability_runtime.TestCapability"
        ),
        dependencies=frozenset(),
    )


def _runtime():
    registry = CapabilityRegistry(
        capabilities=(_capability(),)
    )

    executor = CapabilityExecutor(
        registry=registry,
    )

    return CapabilityRuntime(
        executor=executor,
    )


def test_runtime_executes_capability():
    runtime = _runtime()

    request = CapabilityExecutionRequest(
        capability_id="test.capability",
        input_data="hello",
    )

    result = runtime.execute(request)

    assert isinstance(
        result,
        CapabilityExecutionResult,
    )
    assert result.capability_id == "test.capability"
    assert result.output == {
        "received": "hello",
    }


def test_runtime_preserves_capability_id():
    runtime = _runtime()

    request = CapabilityExecutionRequest(
        capability_id="test.capability",
        input_data=42,
    )

    result = runtime.execute(request)

    assert result.capability_id == request.capability_id


def test_runtime_preserves_executor_output():
    runtime = _runtime()

    input_data = {
        "query": "test",
        "limit": 5,
    }

    request = CapabilityExecutionRequest(
        capability_id="test.capability",
        input_data=input_data,
    )

    result = runtime.execute(request)

    assert result.output == {
        "received": input_data,
    }


def test_runtime_rejects_invalid_executor():
    with pytest.raises(TypeError):
        CapabilityRuntime(
            executor="invalid",
        )


def test_runtime_rejects_invalid_request():
    runtime = _runtime()

    with pytest.raises(TypeError):
        runtime.execute(
            request="invalid",
        )


def test_runtime_propagates_executor_exception():
    registry = CapabilityRegistry()

    executor = CapabilityExecutor(
        registry=registry,
    )

    runtime = CapabilityRuntime(
        executor=executor,
    )

    request = CapabilityExecutionRequest(
        capability_id="missing.capability",
        input_data=None,
    )

    with pytest.raises(KeyError):
        runtime.execute(request)

def test_runtime_delegates_execution_to_existing_executor():
    runtime = _runtime()

    request = CapabilityExecutionRequest(
        capability_id="test.capability",
        input_data="delegated",
    )

    result = runtime.execute(request)

    assert result == CapabilityExecutionResult(
        capability_id="test.capability",
        output={
            "received": "delegated",
        },
    )

def test_runtime_executes_capability_with_explicit_contracts():
    capability = CapabilityDescriptor(
        id="test.capability",
        name="Test Capability",
        description="Test capability.",
        version="1.0.0",
        entry_point=(
            "tests.capabilities.test_capability_runtime.TestCapability"
        ),
        dependencies=frozenset(),
        input_contract="text",
        output_contract="number",
    )

    registry = CapabilityRegistry(
        capabilities=(capability,),
    )

    executor = CapabilityExecutor(
        registry=registry,
    )

    runtime = CapabilityRuntime(
        executor=executor,
    )

    request = CapabilityExecutionRequest(
        capability_id="test.capability",
        input_data="hello",
    )

    result = runtime.execute(request)

    assert result == CapabilityExecutionResult(
        capability_id="test.capability",
        output={
            "received": "hello",
        },
    )

    registered = registry.get(
        "test.capability"
    )

    assert registered.input_contract == "text"
    assert registered.output_contract == "number"

def test_runtime_does_not_modify_capability_contracts():
    capability = CapabilityDescriptor(
        id="test.capability",
        name="Test Capability",
        description="Test capability.",
        version="1.0.0",
        entry_point=(
            "tests.capabilities.test_capability_runtime.TestCapability"
        ),
        dependencies=frozenset(),
        input_contract="text",
        output_contract="number",
    )

    registry = CapabilityRegistry(
        capabilities=(capability,),
    )

    executor = CapabilityExecutor(
        registry=registry,
    )

    runtime = CapabilityRuntime(
        executor=executor,
    )

    request = CapabilityExecutionRequest(
        capability_id="test.capability",
        input_data="hello",
    )

    runtime.execute(request)

    assert capability.input_contract == "text"
    assert capability.output_contract == "number"
    assert registry.get("test.capability") is capability

def test_runtime_propagates_capability_exception():
    capability = CapabilityDescriptor(
        id="failing.capability",
        name="Failing Capability",
        description="Test capability.",
        version="1.0.0",
        entry_point=(
            "tests.capabilities.test_capability_runtime."
            "FailingCapability"
        ),
        dependencies=frozenset(),
    )

    registry = CapabilityRegistry(
        capabilities=(capability,),
    )

    executor = CapabilityExecutor(
        registry=registry,
    )

    runtime = CapabilityRuntime(
        executor=executor,
    )

    request = CapabilityExecutionRequest(
        capability_id="failing.capability",
        input_data="hello",
    )

    with pytest.raises(
        RuntimeError,
        match="capability failed",
    ):
        runtime.execute(request)

def test_runtime_propagates_missing_capability_error():
    registry = CapabilityRegistry()

    executor = CapabilityExecutor(
        registry=registry,
    )

    runtime = CapabilityRuntime(
        executor=executor,
    )

    request = CapabilityExecutionRequest(
        capability_id="missing.capability",
        input_data="hello",
    )

    with pytest.raises(
        KeyError,
        match="capability not found",
    ):
        runtime.execute(request)

def test_runtime_propagates_invalid_capability_id_error():
    registry = CapabilityRegistry()

    executor = CapabilityExecutor(
        registry=registry,
    )

    runtime = CapabilityRuntime(
        executor=executor,
    )

    request = CapabilityExecutionRequest(
        capability_id="",
        input_data="hello",
    )

    with pytest.raises(
        ValueError,
        match="capability_id must not be empty",
    ):
        runtime.execute(request)

def test_integrated_capability_executes_through_runtime():
    capability = CapabilityDescriptor(
        id="integrated.capability",
        name="Integrated Capability",
        description="Test capability.",
        version="1.0.0",
        entry_point=(
            "tests.capabilities.test_capability_runtime."
            "IntegratedCapability"
        ),
        dependencies=frozenset(),
        input_contract="text",
        output_contract="object",
    )

    registry = CapabilityRegistry()

    integrator = CapabilityIntegrator(
        registry=registry,
    )

    integrator.integrate(
        capability=capability,
        verification_passed=True,
    )

    executor = CapabilityExecutor(
        registry=registry,
    )

    runtime = CapabilityRuntime(
        executor=executor,
    )

    request = CapabilityExecutionRequest(
        capability_id="integrated.capability",
        input_data="hello",
    )

    result = runtime.execute(request)

    assert result.capability_id == "integrated.capability"
    assert result.output == {
        "processed": "hello",
    }

    registered = registry.get(
        "integrated.capability"
    )

    assert registered is capability
    assert registered.input_contract == "text"
    assert registered.output_contract == "object"

def test_unverified_capability_cannot_reach_runtime():
    capability = CapabilityDescriptor(
        id="unverified.capability",
        name="Unverified Capability",
        description="Test capability.",
        version="1.0.0",
        entry_point=(
            "tests.capabilities.test_capability_runtime."
            "IntegratedCapability"
        ),
        dependencies=frozenset(),
    )

    registry = CapabilityRegistry()

    integrator = CapabilityIntegrator(
        registry=registry,
    )

    with pytest.raises(ValueError):
        integrator.integrate(
            capability=capability,
            verification_passed=False,
        )

    assert registry.has(
        "unverified.capability"
    ) is False

def test_runtime_uses_existing_executor_registry():
    capability = CapabilityDescriptor(
        id="shared.registry.capability",
        name="Shared Registry Capability",
        description="Test capability.",
        version="1.0.0",
        entry_point=(
            "tests.capabilities.test_capability_runtime."
            "IntegratedCapability"
        ),
        dependencies=frozenset(),
    )

    registry = CapabilityRegistry(
        capabilities=(capability,),
    )

    executor = CapabilityExecutor(
        registry=registry,
    )

    runtime = CapabilityRuntime(
        executor=executor,
    )

    request = CapabilityExecutionRequest(
        capability_id="shared.registry.capability",
        input_data="test",
    )

    result = runtime.execute(request)

    assert result.output == {
        "processed": "test",
    }

    assert registry.get(
        "shared.registry.capability"
    ) is capability